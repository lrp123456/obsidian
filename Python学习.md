# Python 学习大纲

## 一、基础语法

### 1. 环境与基础
- Python 解释器与版本（Python 2 vs Python 3）
- 交互式环境（REPL）与脚本执行
- 编码规范（PEP 8）与 Pythonic 实践
  - **核心命名**：Python 倾向 `snake_case`，类名使用 `PascalCase`（同 Java）。
  - **空白逻辑**：严格 4 空格缩进，顶层定义空 2 行，方法内空 1 行。
  - **Docstrings (Agent 核心)**：函数的文档字符串是工具描述的来源，需符合 PEP 257。
  - **工具链**：推荐使用 Ruff (Linter) + Black (Formatter) + MyPy (Type Check)。
- 注释与文档字符串规范

### 2. 变量与数据类型 (Type Resilience)

> [!TIP] Java 开发者迁移视角
> Python 是典型的“鸭子类型”。在 Agent 开发中，我们通过 **Type Hints** 重新找回 Java 的静态类型安全性。

#### 2.1 动态类型与类型提示 (Type Hints)
*   **变量声明**：从 Java 的强约束到 Python 的暗示。
    *   Python: `age: int = 25` (仅做提示，运行期不强制)
    *   Java 相邻概念：类似 `var` (Java 10+)，但 Python 更加动态。
*   **常用标准类型**：`int`, `float`, `bool`, `str`, `bytes` (Agent 序列化常用)。
*   **复合类型 (typing 模块)**：`List[str]`, `Dict[str, Any]`, `Optional[int]` (对应 Java 的 `List<String>`, `Map<String, Object>`, `Optional<Integer>`)。

#### 2.2 字符串——Agent 的主要语言
*   **f-string (推荐)**：极其强大的格式化语法。
    ```python
    prompt = f"Hello {user_name}, your balance is {amount:.2f}"
    ```
*   **多行字符串**：用 `"""文本"""` 定义 Prompt 模板。
*   **字节串 (bytes)**：Agent 处理图像、语音等非文本数据时的原始格式。

#### 2.3 类型检查与转换
*   **自省工具**：
    *   `type(obj)`: 查看对象类型。
    *   `isinstance(obj, Class)`: **推荐用法**，支持继承链检查（类似 Java 的 `instanceof`）。
*   **强制转换**：`int()`, `str()`, `list()` 等构造函数。

#### 2.4 Pydantic 进阶预告 (Agent 数据底座)
*   **为什么不用原生 class？** 因为 Agent 需要在接收到模型的 JSON 输出时实现“自动校验”与“自动解析”。这部分将在《数据处理》章节详解。

---

### 3. 运算符
- 算术运算符（+, -, *, /, //, %, **）
- 比较运算符（==, !=, >, <, >=, <=）
- 逻辑运算符（and, or, not）
- 位运算符（&, |, ^, ~, <<, >>）
- 赋值运算符与复合赋值
- 成员运算符（in, not in）
- 身份运算符（is, is not）
- 运算符优先级

### 4. 字符串操作
- 字符串创建与引号使用
- 字符串索引与切片
- 字符串方法（upper, lower, strip, split, join, replace, find, format 等）
- 格式化字符串（%, format(), f-string）
- 原始字符串与转义字符
- 字符串编码与解码

### 5. 数据结构
#### 5.1 列表（List）
- 创建与访问
- 增删改查操作
- 列表方法（append, extend, insert, remove, pop, sort, reverse 等）
- 列表推导式
- 列表切片

#### 5.2 元组（Tuple）
- 创建与访问
- 不可变性
- 解包操作
- 命名元组（namedtuple）

#### 5.3 集合（Set）
- 创建与特点（无序、唯一）
- 集合运算（交集、并集、差集、对称差）
- 集合方法
- 集合推导式

#### 5.4 字典（Dict）
- 创建与访问
- 增删改查操作
- 字典方法（keys, values, items, get, update, pop 等）
- 字典推导式
- 嵌套字典

### 6. 流程控制
#### 6.1 条件语句
- if 语句
- if-else 语句
- if-elif-else 语句
- 条件表达式（三元运算符）

#### 6.2 循环语句
- while 循环
- for 循环
- range() 函数
- break、continue、pass
- 循环的 else 子句
- 循环嵌套

### 7. 函数基础
- 函数定义与调用
- 参数传递
  - 位置参数
  - 关键字参数
  - 默认参数
  - 可变位置参数（*args）
  - 可变关键字参数（**kwargs）
- 返回值与多返回值
- 变量作用域（局部、全局、nonlocal）
- 递归函数
- lambda 表达式

### 8. 输入输出
- input() 函数
- print() 函数
- 文件读写
  - open() 函数
  - 文件模式（r, w, a, b, +）
  - with 语句（上下文管理器）
  - 文件对象方法（read, readline, readlines, write, writelines）

### 9. 异常处理
- try-except 语句
- 异常类型（Exception, ValueError, TypeError 等）
- 多异常捕获
- else 和 finally 子句
- raise 语句
- 自定义异常类
- assert 断言

### 10. 模块与包
- import 语句
- from...import 语句
- 模块搜索路径
- __name__ 与 __main__
- 包的结构与 __init__.py
- 第三方库安装（pip）

---

## 二、高级语法

### 1. 面向对象编程（OOP）
#### 1.1 类与对象
- 类的定义与实例化
- 构造函数 __init__
- 实例属性与类属性
- 实例方法、类方法（@classmethod）、静态方法（@staticmethod）

#### 1.2 封装
- 访问控制（公有、保护、私有）
- 属性装饰器（@property）

#### 1.3 继承
- 单继承与多继承
- super() 函数
- 方法重写
- MRO（方法解析顺序）
- 抽象基类（ABC）

#### 1.4 多态
- 鸭子类型
- 接口与协议

#### 1.5 特殊方法（魔术方法）
- __str__, __repr__
- __len__, __bool__
- __getitem__, __setitem__, __delitem__
- __iter__, __next__
- __enter__, __exit__
- __call__
- __eq__, __lt__, __gt__ 等比较运算符
- __add__, __sub__, __mul__ 等算术运算符

### 2. 迭代器与生成器
#### 2.1 迭代器
- 迭代器协议（__iter__, __next__）
- iter() 与 next() 函数
- 自定义迭代器

#### 2.2 生成器
- 生成器函数（yield）
- 生成器表达式
- yield from 语法
- 生成器状态与方法（send, throw, close）

### 3. 装饰器
- 装饰器原理与语法糖
- 函数装饰器
- 带参数的装饰器
- 类装饰器
- 装饰器链
- functools.wraps 保留元信息
- 常用内置装饰器（@property, @classmethod, @staticmethod）

### 4. 上下文管理器
- with 语句原理
- __enter__ 与 __exit__ 方法
- contextlib 模块
- @contextmanager 装饰器

### 5. 元编程
#### 5.1 动态特性
- 动态创建类（type()）
- __slots__ 限制属性
- 动态属性（__getattr__, __setattr__, __delattr__）

#### 5.2 描述符
- 描述符协议（__get__, __set__, __delete__）
- 描述符应用

#### 5.3 元类
- type 作为元类
- 自定义元类（__new__, __init__, __call__）
- __metaclass__（Python 2）与 metaclass 参数

### 6. 高级函数特性
- 闭包
- 高阶函数（map, filter, reduce）
- 偏函数（functools.partial）
- 函数注解与类型提示
- 可调用对象（__call__）

### 7. 异步编程
#### 7.1 协程基础
- 协程概念
- async/await 语法
- async def 定义协程
- await 等待协程

#### 7.2 异步编程工具
- asyncio 模块
- 事件循环（Event Loop）
- async with 异步上下文管理
- async for 异步迭代器
- 并发执行（gather, wait, create_task）

#### 7.3 异步库
- aiohttp 异步 HTTP
- 异步数据库驱动

### 8. 并发与并行
#### 8.1 多线程
- threading 模块
- Thread 类
- 线程同步（Lock, RLock, Semaphore, Event, Condition）
- 线程池（ThreadPoolExecutor）
- GIL（全局解释器锁）

#### 8.2 多进程
- multiprocessing 模块
- Process 类
- 进程间通信（Queue, Pipe, Shared Memory）
- 进程池（ProcessPoolExecutor）

#### 8.3 concurrent.futures
- Future 对象
- Executor 抽象类
- submit() 与 map()

### 9. 类型系统（Type Hints）
- 基本类型注解
- typing 模块
  - List, Dict, Set, Tuple
  - Optional, Union
  - Callable, Any
  - TypeVar, Generic
  - Protocol
- 类型别名
- @overload 装饰器
- 类型检查工具（mypy）

### 10. 内存管理与性能优化
#### 10.1 内存管理
- 引用计数
- 垃圾回收机制（GC）
- gc 模块
- 内存视图（memoryview）
- 弱引用（weakref）

#### 10.2 性能优化
- 时间复杂度与空间复杂度
- timeit 模块测量性能
- cProfile 性能分析
- 数据结构选择
- 算法优化

### 11. 反射与内省
- dir() 查看属性
- hasattr(), getattr(), setattr(), delattr()
- vars() 与 __dict__
- inspect 模块
- __doc__ 与 help()

### 12. 代码组织与设计模式
#### 12.1 代码组织
- 项目结构规范
- 模块化设计
- 代码复用

#### 12.2 常用设计模式
- 单例模式
- 工厂模式
- 观察者模式
- 策略模式
- 装饰器模式
- 适配器模式

### 13. 测试
- unittest 模块
- pytest 框架
- 测试驱动开发（TDD）
- Mock 与 Patch
- 覆盖率测试

### 14. 高级数据处理
- 正则表达式（re 模块）
- 序列化与反序列化（pickle, json）
- 数据类（@dataclass）
- 枚举类（enum 模块）
- collections 模块（Counter, deque, defaultdict, OrderedDict）

### 15. 网络编程
- socket 编程基础
- HTTP 请求（requests 库）
- Web 开发框架（Flask, Django, FastAPI）
- RESTful API 设计

### 16. 数据库编程
- SQLite 操作
- ORM 框架（SQLAlchemy）
- 数据库连接池

---

## 三、学习路径建议

```
基础阶段（1-2个月）
├── 环境搭建与基础语法
├── 数据类型与数据结构
├── 流程控制
└── 函数基础

进阶阶段（2-3个月）
├── 面向对象编程
├── 模块与包
├── 文件操作与异常处理
└── 常用标准库

高级阶段（3-6个月）
├── 装饰器与生成器
├── 异步编程
├── 并发编程
├── 元编程
└── 类型系统

实战阶段（持续）
├── 项目开发
├── 测试与调试
├── 性能优化
└── 框架学习
```

---

## 四、推荐资源

### 官方文档
- [Python 官方文档](https://docs.python.org/zh-cn/3/)
- [PEP 索引](https://peps.python.org/)

### 经典书籍
- 《Python编程：从入门到实践》
- 《流畅的Python》
- 《Python Cookbook》
- 《Effective Python》

### 在线练习
- LeetCode（算法练习）
- Codewars（编程挑战）
- HackerRank（技能认证）
