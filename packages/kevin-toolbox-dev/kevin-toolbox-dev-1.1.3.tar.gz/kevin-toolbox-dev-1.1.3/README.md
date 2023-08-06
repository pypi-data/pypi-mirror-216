# kevin_toolbox

一个通用的工具代码包集合



环境要求

```shell
numpy>=1.19
pytorch>=1.2
```

安装方法：

```shell
pip install kevin-toolbox  --no-dependencies
```



[项目地址 Repo](https://github.com/cantbeblank96/kevin_toolbox)

[使用指南 User_Guide](./notes/User_Guide.md)

[免责声明 Disclaimer](./notes/Disclaimer.md)

[版本更新记录](./notes/Release_Record.md)：

- v 1.1.3（2023-06-30）
  - computer_science.algorithm.for_nested_dict_list
    - 在 traverse() 中新增了traversal_mode 参数用于控制遍历的顺序，目前支持三种模式： "dfs_pre_order" 深度优先-先序遍历、"dfs_post_order" 深度优先-后序遍历、以及 "bfs" 宽度优先。
      - 在单元测试中新增了对 traverse() 中 traversal_mode 参数的测试项目。
    - value_parser
      - 修改 eval_references() 中 converter_for_ref 参数的行为，从原来只是作为计算结果前对算式中引用节点值的预处理，变成直接改变被引用节点的值。亦即原来不会修改原被引用节点的值，现在变为会修改原节点的值了。
  - computer_science.algorithm.scheduler
    - 改进 Strategy_Manager
      - 使用 `<eval>` 来标记需要使用 eval() 函数读取的字符串。相对于旧版通过 `<eval>` 来标记需要被读取为函数的字符串，使用 `<eval>` 不仅可以读取函数，也可以读取更多的数据结构。
      - 在通过 add() 添加策略时即对 strategy 中被 `<eval>` 标记的键值进行解释，而非等到后续每次 cal() 时再进行解释，提高了效率。
      - 修改了对应的单元测试。
