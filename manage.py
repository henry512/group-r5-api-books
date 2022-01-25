from uvicorn import run
from src.app import app
import logging


if __name__ == '__main__':
    host = app.container.config.get("deploy")["host"]
    port = app.container.config.get("deploy")["port"] 
    log_level = app.container.config.get("deploy")["log_level"] 
    workers = app.container.config.get("deploy")["workers"]
    """
    Generate Banner ASCII
    URL: https://patorjk.com/software/taag/#p=display&v=1&c=bash&f=ANSI%20Shadow&t=GROUP%20R5%0AApi%20Books%20%20v.1.0.0
    """
    print(f"""

    ██████╗ ██████╗  ██████╗ ██╗   ██╗██████╗         ██████╗ ███████╗
    ██╔════╝ ██╔══██╗██╔═══██╗██║   ██║██╔══██╗        ██╔══██╗██╔════╝
    ██║  ███╗██████╔╝██║   ██║██║   ██║██████╔╝        ██████╔╝███████╗
    ██║   ██║██╔══██╗██║   ██║██║   ██║██╔═══╝         ██╔══██╗╚════██║
    ╚██████╔╝██║  ██║╚██████╔╝╚██████╔╝██║             ██║  ██║███████║
    ╚═════╝ ╚═╝  ╚═╝ ╚═════╝  ╚═════╝ ╚═╝             ╚═╝  ╚═╝╚══════╝
    
     █████╗ ██████╗ ██╗    ██████╗  ██████╗  ██████╗ ██╗  ██╗███████╗ 
    ██╔══██╗██╔══██╗██║    ██╔══██╗██╔═══██╗██╔═══██╗██║ ██╔╝██╔════╝
    ███████║██████╔╝██║    ██████╔╝██║   ██║██║   ██║█████╔╝ ███████╗
    ██╔══██║██╔═══╝ ██║    ██╔══██╗██║   ██║██║   ██║██╔═██╗ ╚════██║
    ██║  ██║██║     ██║    ██████╔╝╚██████╔╝╚██████╔╝██║  ██╗███████║
    ╚═╝  ╚═╝╚═╝     ╚═╝    ╚═════╝  ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚══════╝
    
    @hot= {host}
    @port= {port}
    @workers= {workers}
    @log_level= {log_level}
    @maintainer= {app.container.config.get("info")["maintainer"]}
    @version= {app.container.config.get("info")["version"]}
    """)
    
    run(
        "manage:app", 
        host=host, 
        port=port, 
        log_level=log_level, 
        reload=False, 
        workers=workers
    )
