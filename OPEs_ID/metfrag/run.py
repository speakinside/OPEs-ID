import asyncio
import dataclasses
import sys
import threading
from pathlib import Path

import pandas as pd
from ..mtype import check_progress, ProgressFunc
from .param import MetFragParameter
from .config import RuntimeConfig as _config


@dataclasses.dataclass(slots=True)
class MetFragFailed:
    returncode: int
    stdout: str
    stderr: str


async def progress_gather(*fs, progress: ProgressFunc | bool = True):
    async def wrap_awaitable(i, f):
        return i, await f

    progress = check_progress(progress)

    ifs = [wrap_awaitable(i, f) for i, f in enumerate(fs)]
    res = [await f for f in progress(asyncio.as_completed(ifs), total=len(ifs))]

    return [r for _, r in sorted(res, key=lambda x: x[0])]


class RunThread(threading.Thread):
    def __init__(self, func, *args, **kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs

        super().__init__()

    def run(self):
        loop = asyncio.ProactorEventLoop()
        asyncio.set_event_loop(loop)
        self.result = loop.run_until_complete(self.func(*self.args, **self.kwargs))


class AsyncMetFragPool:
    def __init__(self, n_jobs=8, progress: ProgressFunc | bool = True) -> None:
        self.n_jobs = n_jobs
        self.progress = progress

    def __call__(self, parameters: list["MetFragParameter"]):
        JAVA_EXE = _config.get_java_exe()
        METFRAG_EXE = _config.get_metfrag_path()

        async def main():
            semaphore = asyncio.Semaphore(self.n_jobs)

            async def metfrag(param: MetFragParameter):
                nonlocal semaphore, JAVA_EXE, METFRAG_EXE

                if param.m_ParamSavePath is not None:
                    param.dump(param.m_ParamSavePath)
                if param.ResultsPath:
                    Path(param.ResultsPath).mkdir(parents=True, exist_ok=True)
                async with semaphore:
                    param_save_path = Path(param.m_ParamSavePath)

                    proc = await asyncio.create_subprocess_exec(
                        JAVA_EXE,
                        "-jar",
                        METFRAG_EXE,
                        param_save_path.name,
                        stdout=asyncio.subprocess.PIPE,
                        stderr=asyncio.subprocess.PIPE,
                        cwd=param_save_path.parent,
                    )
                    stdout, stderr = await proc.communicate()

                if proc.returncode != 0:
                    return MetFragFailed(
                        proc.returncode,
                        stdout.decode(errors="ignore"),
                        stderr.decode(errors="ignore"),
                    )
                else:
                    if param.MetFragCandidateWriter == "XLS":
                        return pd.read_excel(
                            Path(param.ResultsPath)
                            / f"{param.SampleName}.{param.MetFragCandidateWriter}"
                        )
                    elif param.MetFragCandidateWriter == "CSV":
                        return pd.read_csv(
                            Path(param.ResultsPath)
                            / f"{param.SampleName}.{param.MetFragCandidateWriter}"
                        )

            return await progress_gather(
                *[metfrag(p) for p in parameters], progress=self.progress
            )

        try:
            loop = asyncio.get_running_loop()
            exsiting = True
        except RuntimeError:
            loop = asyncio.new_event_loop()
            exsiting = False

        if sys.platform == "win32" and isinstance(loop, asyncio.SelectorEventLoop):
            if not exsiting:
                loop.close()
            import nest_asyncio
            loop = asyncio.ProactorEventLoop()
            nest_asyncio.apply(loop)
        
        results = loop.run_until_complete(main())
        if not exsiting:
            loop.close()
        return results

                

