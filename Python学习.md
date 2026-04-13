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

### 3. 运算符 (Operators & Logic)

> [!TIP] Java 开发者迁移视角
> Python 的运算符中，`is` 和 `==` 的区别是重灾区，类似于 Java 的 `==` vs `.equals()`。

#### 3.1 算术运算符：除法有坑
*   **`/` (真除法)**：`5 / 2` 结果是 `2.5`。即使是整数相除，结果也会自动转为 `float`。
*   **`//` (整除/地板除)**：`5 // 2` 结果是 `2`。这才是 Java 开发习惯的整数相除。
*   **`**` (幂运算)**：`2 ** 3` 结果是 `8`。不再需要调用 `Math.pow()`。
*   **`%` (取模)**：同 Java。

#### 3.2 比较运算符：内容 vs 内存
*   **`==` (值比较)**：检查内容是否等价。相当于 Java 的 `obj1.equals(obj2)`。
*   **`is` (身份比较)**：检查是否为同一个内存地址。相当于 Java 的 `obj1 == obj2`。
    *   *Agent 场景提示*：检查变量是否为 `None`（空值）时，标准写法是 `if x is None:`。

#### 3.3 逻辑运算符：单词替代符号
*   使用 `and`, `or`, `not` 替代 Java 的 `&&`, `||`, `!`。
*   **短路特性**：与 Java 一致。

#### 3.4 赋值运算符与“海象”运算符
*   **海象运算符 `:=` (Python 3.8+)**：允许在表达式中赋值。
    *   *Agent 场景*：在 `while` 循环中同时读取 LLM 的流式响应并检查状态。
    ```python
    while (content := await response.read()):
        process(content)
    ```

#### 3.5 成员与身份 (Pythonic 糖)
*   **`in` / `not in`**：检查元素是否在集合/列表中（类似 Java 中调用 `list.contains()`）。
*   **`is` / `is not`**：身份判断。

---

### 4. 字符串操作 (Agent 的文本引擎)

> [!TIP] Java 开发者视角
> Python 的字符串是 **Unicode 不可变序列**，类似 Java 的 `String`（不可变特性相同）。但 Python 没有 StringBuilder，所有字符串操作返回新字符串。

#### 4.1 字符串创建与引号使用

```python
# 单引号、双引号 - 等价
name = 'Alice'
name = "Alice"

# 三引号 - 多行字符串（Prompt 模板常用）
prompt = """
你是一个助手。
用户说：{user_input}
"""

# 相邻字符串自动拼接（类比 JavaScript）
message = ("这是第一部分"
           "这是第二部分")  # 等同于 "这是第一部分这是第二部分"
```

**Java 对比**：
```java
// Java 需要 + 号拼接
String message = "第一部分" + "第二部分";
// 多行字符串（Java 15+）
String prompt = """
    你是一个助手。
    用户说：{user_input}
    """;
```

#### 4.2 字符串索引与切片

> [!WARNING] 索引越界
> Python 索引越界会抛出 `IndexError`，不会像某些语言返回 null。

```python
text = "Hello, Python!"

# 索引访问（0-based，与 Java 相同）
print(text[0])   # 'H'
print(text[7])   # 'P'
print(text[-1])  # '!'（负数从末尾开始）

# 切片 [start:end:step]
print(text[0:5])      # 'Hello'
print(text[7:13])     # 'Python'
print(text[:5])       # 'Hello'（省略 start = 0）
print(text[7:])       # 'Python!'（省略 end = 末尾）
print(text[::2])      # 'Hlo yhn'（步长 2）
print(text[::-1])     # '!nohtyP ,olleH'（反转）

# 切片越界不报错（与 Java 不同）
print(text[0:100])   # 'Hello, Python!'（安全访问）
```

**切片原理**：
```
字符串:  H  e    l    l     o     ,     P  y  t  h  o     n      !
索引:    0  1    2    3     4     5     6  7  8  9 10 11 12  13
负索引: -14 -13 -12  -11   -10    -9    -8 -7 -6 -5 -4 -3 -2 -1
```

#### 4.3 字符串方法（Agent 开发核心）

> [!TIP] 重要特性
> Python 字符串方法**不修改原字符串**，而是返回新字符串。这是 immutable 特性决定的。

##### 大小写转换

```python
text = "Hello, World!"

text.upper()           # 'HELLO, WORLD!'（全大写）
text.lower()           # 'hello, world!'（全小写）
text.capitalize()      # 'Hello, world!'（首字母大写）
text.title()           # 'Hello, World!'（每个词首字母大写）
text.swapcase()        # 'hELLO, wORLD!'（大小写互换）
```

##### 查找与计数

```python
text = "Hello, World! Hello Python!"

text.find("World")      # 7（首次出现的索引，未找到返回 -1）
text.find("World", 10)  # -1（从索引 10 开始查找）
text.rfind("Hello")     # 13（从右向左查找）
text.index("World")     # 7（类似 find，但未找到抛出 ValueError）
text.count("Hello")     # 2（计数）
text.count("o")         # 4
```

##### 开头与结尾判断

```python
url = "https://api.example.com/v1/chat"

url.startswith("https://")   # True
url.startswith(("http://", "https://"))  # True（元组形式）
url.endswith(".com")         # True
url.endswith((".com", ".org", ".io"))     # True
```

##### 去除空白

```python
text = "  Hello, World!  \n"

text.strip()     # 'Hello, World!  \n'（去除两端空白和换行）
text.lstrip()    # 'Hello, World!  \n'（仅去除左侧）
text.rstrip()    # '  Hello, World!'（仅去除右侧）
text.strip('\n') # '  Hello, World!  '（去除指定字符）
```

##### 分割与连接

```python
# split - 分割
text = "apple,banana,cherry"
text.split(',')              # ['apple', 'banana', 'cherry']
text.split(',', maxsplit=1)  # ['apple', 'banana,cherry']（限制分割次数）

# rsplit - 从右向左分割
text.rsplit(',', maxsplit=1) # ['apple,banana', 'cherry']

# splitlines - 按行分割
text = "Line1\nLine2\r\nLine3"
text.splitlines()  # ['Line1', 'Line2', 'Line3']

# partition - 返回 (前, 分隔符, 后)
text.partition(',')  # ('apple', ',', 'banana,cherry')

# join - 连接（Agent 拼接 Prompt 常用）
words = ['Hello', 'World', '!']
' '.join(words)      # 'Hello World !'
'\n'.join(words)     # 'Hello\nWorld\n!'
```

##### 替换

```python
text = "Hello, World!"

text.replace("World", "Python")           # 'Hello, Python!'
text.replace("o", "0")                    # 'Hell0, W0rld!'
text.replace("o", "0", 1)                 # 'Hell0, World!'（仅替换 1 次）

# replace 多重替换（链式调用）
text.replace("Hello", "Hi").replace("World", "Python")
```

##### 判断类型

```python
text = "Hello123"

text.isalpha()    # False（包含数字）
"Hello".isalpha() # True
"123".isdigit()   # True
"3.14".isdigit()  # False（点号不是数字）
"3.14".isdecimal() # False（用于 Unicode 数字）
"Hello123".isalnum()    # True（字母或数字）
"Hello World".isspace() # False
"   ".isspace()   # True
```

##### 填充与对齐

```python
text = "42"

text.zfill(6)       # '000042'（零填充）
text.rjust(6, '0')  # '000042'（右对齐）
text.ljust(6, '0')  # '420000'（左对齐）
text.center(6, '*') # '**42**'（居中）
```

#### 4.4 格式化字符串

##### f-string（Python 3.6+，Agent 开发首选）

```python
name = "Alice"
age = 30
balance = 1234.567

# 基本用法
f"Hello, {name}!"                                    # 'Hello, Alice!'

# 表达式
f"{name} is {age} years old"                         # 'Alice is 30 years old'

# 格式说明符
f"Balance: {balance:.2f}"                            # 'Balance: 1234.57'
f"Hex: {255:#x}, Binary: {255:#b}"                   # 'Hex: 0xff, Binary: 0b11111111'

# 调试格式（快速输出变量名和值）
x = 10
f"{x=}"    # 'x=10'
f"{x + 5=}"  # 'x + 5=15'

# 引用属性和方法
f"{name.upper()}"                                    # 'ALICE'
f"{len(name)}"                                      # '5'

# 格式转换
f"{'text'!r}"    # "'text'"（repr 格式）
f"{'text'!s}"    # 'text'（str 格式）
f"{'text'!a}"    # "'text'"（ASCII 格式）
```

##### str.format()（Python 2.6+）

```python
# 位置参数
"Hello, {}! Today is {}".format("Alice", "Monday")
# 'Hello, Alice! Today is Monday'

# 索引
"Item {0}: {1}, Item {0}: {2}".format("A", "B", "C")
# 'Item A: B, Item A: C'

# 关键字参数
"Hello, {name}! Your score is {score}".format(name="Alice", score=95)
# 'Hello, Alice! Your score is 95'

# 格式说明符
"{:.2f}".format(3.14159)     # '3.14'
"{:>10}".format("right")      # '     right'（右对齐）
"{:<10}".format("left")       # 'left      '（左对齐）
"{:^10}".format("center")     # '  center  '（居中）
"{:*>10}".format("pad")        # '******pad'（填充字符）
```

##### % 格式化（旧式，类比 C printf）

```python
# %s - 字符串
"Hello, %s!" % "Alice"           # 'Hello, Alice!'

# %d - 整数
"Count: %d" % 42                 # 'Count: 42'

# %f - 浮点数
"Value: %.2f" % 3.14159          # 'Value: 3.14'

# %x, %o, %b - 进制转换
"%x" % 255                       # 'ff'
"%o" % 255                       # '377'
"%b" % 255                       # '11111111'

# 多值
"(%d, %s)" % (42, "items")       # '(42, items)'
```

> [!TIP] Agent 开发推荐
> **f-string 是首选**，性能最佳（Python 3.6+ 内部优化）。对于复杂模板，使用模板引擎如 `string.Template`。

##### Prompt 模板实战

```python
# Agent 的典型 Prompt 构建
system_prompt = """你是一个专业的{role}。

你的职责：
{responsibilities}

回答要求：
- 语言风格：{style}
- 输出格式：{format}
"""

responsibilities = "\n".join([
    f"- {i+1}. {r}" 
    for i, r in enumerate(["回答问题", "提供建议", "解决问题"])
])

prompt = system_prompt.format(
    role="技术助手",
    responsibilities=responsibilities,
    style="专业且友好",
    format="简洁明了"
)

# f-string 版本（更简洁）
tools = ["搜索", "计算", "转换"]
prompt = f"""你是一个助手。
可用工具：{', '.join(tools)}
用户问题：{{user_question}}
"""
```

#### 4.5 原始字符串与转义字符

##### 转义字符

```python
# 常用转义
print("Line1\nLine2")   # 换行
print("Col1\tCol2")      # Tab
print("Path\\n")         # 反斜杠
print('She said: "Hi"')  # 双引号
print("He said: 'Hi'")   # 单引号
print("\u4E2D\u6587")    # Unicode 中文
print("\u2764")          # ❤️

# 取消转义
print(r"Path\ntest")     # Path\ntest（raw string）
```

##### 原始字符串 r"..."

```python
# 文件路径处理（Windows/Linux 通用）
windows_path = r"C:\Users\Admin\Documents"
linux_path = r"/home/user/docs"

# 正则表达式（极其重要）
import re
pattern = r"\d+\.\d+"  # 匹配数字如 3.14
text = "Pi is 3.14159"
re.findall(pattern, text)  # ['3.14159']
```

> [!WARNING] 原始字符串的坑
> 原始字符串**不能以反斜杠结尾**：
> ```python
> path = r"C:\Users\"     # SyntaxError!
> path = r"C:\Users" + "\\"  # 正确写法
> ```

#### 4.6 字符串编码与解码

> [!TIP] Agent 开发重点
> LLM 输出、API 通信、文件读写都涉及编码。`utf-8` 是标准。

```python
# Unicode 编码
text = "你好，世界！"
encoded = text.encode('utf-8')
print(encoded)  # b'\xe4\xb8\xad\xe6\x96\x87'

# 解码回字符串
decoded = encoded.decode('utf-8')
print(decoded)  # '你好，世界！'

# 其他编码
text.encode('gbk')   # 中文 Windows 常用
text.encode('ascii')  # 仅 ASCII 字符，否则抛出 UnicodeEncodeError
text.encode('ascii', errors='ignore')  # 忽略非 ASCII 字符
text.encode('ascii', errors='replace') # 替换为 ?

# 字节串操作（bytes）
b"Hello"[0]          # 72（返回整数）
b"Hello"[0:2]       # b'He'
b"Hello".decode()   # 'Hello'
```

**常见编码对比**：

| 编码 | 说明 | 使用场景 |
|------|------|----------|
| utf-8 | Unicode 可变长度 | Web/API/文件（推荐） |
| gbk | 中文扩展 | Windows 中文系统 |
| ascii | 7位字符 | 旧系统 |
| iso-8859-1 | Latin-1 | 某些数据库 |

#### 4.7 字符串驻留与比较

```python
# 字符串驻留（类似 Java 的 String Pool）
a = "hello"
b = "hello"
a is b    # True（同一对象）

# 编译时常量会被驻留
x = "hello world"
y = "hello world"
x is y    # 可能 True 或 False（取决于实现）

# 显式驻留
import sys
a = sys.intern("hello world")
b = sys.intern("hello world")
a is b    # True（强制驻留）
```

> [!TIP] 比较规则
> - `==` 比较**内容**：始终使用
> - `is` 比较**身份**：仅用于与 `None` 比较

#### 4.8 字符串与其他类型转换

```python
# 字符串 → 数字
int("42")        # 42
float("3.14")    # 3.14
bool("False")    # True（非空字符串）
bool("")         # False（空字符串）

# 数字 → 字符串
str(42)          # "42"
str(3.14)        # "3.14"
repr(3.14)       # "3.14"（保留精度）

# 列表 → 字符串
list("hello")    # ['h', 'e', 'l', 'l', 'o']
"".join(['h', 'e', 'l', 'l', 'o'])  # 'hello'

# 字符串 → 字节
"text".encode()  # b'text'
b"text".decode() # 'text'
```

#### 4.9 实战：Agent Prompt 模板构建

```python
class PromptBuilder:
    """Agent Prompt 构建器 - 展示字符串操作综合应用"""
    
    def __init__(self):
        self.parts = []
    
    def add_role(self, role: str) -> "PromptBuilder":
        self.parts.append(f"角色：{role}")
        return self
    
    def add_instruction(self, instruction: str) -> "PromptBuilder":
        self.parts.append(f"指令：{instruction}")
        return self
    
    def add_examples(self, examples: list[dict]) -> "PromptBuilder":
        if not examples:
            return self
        example_text = "\n".join(
            f"输入：{e['input']}\n输出：{e['output']}"
            for e in examples
        )
        self.parts.append(f"示例：\n{example_text}")
        return self
    
    def add_constraint(self, constraint: str) -> "PromptBuilder":
        self.parts.append(f"约束：{constraint}")
        return self
    
    def build(self) -> str:
        return "\n\n".join(self.parts)

# 使用
prompt = (
    PromptBuilder()
    .add_role("专业客服")
    .add_instruction("回答用户问题，保持礼貌")
    .add_examples([
        {"input": "你们几点开门？", "output": "我们早上9点开门。"},
        {"input": "有优惠吗？", "output": "本月全场8折。"}
    ])
    .add_constraint("不要透露商业机密")
    .build()
)
```

---

#### 📋 字符串方法速查表

| 方法 | 说明 | 返回值 |
|------|------|--------|
| `s.upper()` | 转大写 | str |
| `s.lower()` | 转小写 | str |
| `s.strip()` | 去除空白 | str |
| `s.split(sep)` | 分割 | list |
| `s.join(iter)` | 连接 | str |
| `s.replace(old, new)` | 替换 | str |
| `s.find(sub)` | 查找位置 | int |
| `s.startswith(s)` | 是否开头 | bool |
| `s.endswith(s)` | 是否结尾 | bool |
| `s.format(**kw)` | 格式化 | str |
| `s.encode()` | 编码 | bytes |
| `len(s)` | 长度 | int |

---

#### 🎯 面试高频考点

1. **Python 字符串是否可变？** - 不可变（immutable），所有操作返回新字符串
2. **f-string、format()、% 的区别？** - f-string 性能最佳，format() 更灵活，% 为旧式
3. **字符串切片 `[::-1]` 的含义？** - 反转字符串
4. **Unicode 和 UTF-8 的关系？** - Unicode 是字符集，UTF-8 是编码实现
5. **bytes 和 str 的区别？** - bytes 是字节序列，str 是 Unicode 字符串

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
