# 项目记忆

当前项目根目录：`C:\Users\chqte\Documents\Codex\KingdeeZwyCashFlowGenerator`。
旧项目路径 `D:\CashFlowGenerator` 已失效；后续文件查找、运行与修改均以当前目录为准。

参考项目：`C:\Users\chqte\Documents\Codex\KingdeeZwyDataAnalyser`。当前优先优化代码结构和可维护性。
源码目录为 `KingdeeZwyCashFlowGenerator/`，按 `app`、`core`、`configuration`、`domain`、`ledger`、`classification`、`quarter`、`reporting` 分类。源码启动入口为 `scripts/run/launch.py`，项目路径集中在 `KingdeeZwyCashFlowGenerator/core/paths.py`；包内模块不自行修改 `sys.path`。
本地检查命令为 `scripts/check/static.ps1`。项目虚拟环境 `.weiyu` 已迁移至 `D:\Python` 解释器。
项目文件按用途存放：`config/config.yaml` 为本机规则，`resources/templates/` 为模板，`resources/icon.ico` 为图标，`packaging/build.spec` 为打包配置，`runtime/` 为输入、输出和日志。修改位置时同步更新 `KingdeeZwyCashFlowGenerator/core/paths.py` 与相关配置。
业务回归测试位于 `tests/`，用 `.weiyu/Scripts/python.exe -m unittest discover -s tests -v` 运行；测试样本和输出放在临时目录，不使用用户明细账。
