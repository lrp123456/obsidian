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

| 方法                    | 说明   | 返回值   |
| --------------------- | ---- | ----- |
| `s.upper()`           | 转大写  | str   |
| `s.lower()`           | 转小写  | str   |
| `s.strip()`           | 去除空白 | str   |
| `s.split(sep)`        | 分割   | list  |
| `s.join(iter)`        | 连接   | str   |
| `s.replace(old, new)` | 替换   | str   |
| `s.find(sub)`         | 查找位置 | int   |
| `s.startswith(s)`     | 是否开头 | bool  |
| `s.endswith(s)`       | 是否结尾 | bool  |
| `s.format(**kw)`      | 格式化  | str   |
| `s.encode()`          | 编码   | bytes |
| `len(s)`              | 长度   | int   |

---

#### 🎯 面试高频考点

1. **Python 字符串是否可变？** - 不可变（immutable），所有操作返回新字符串
2. **f-string、format()、% 的区别？** - f-string 性能最佳，format() 更灵活，% 为旧式
3. **字符串切片 `[::-1]` 的含义？** - 反转字符串
4. **Unicode 和 UTF-8 的关系？** - Unicode 是字符集，UTF-8 是编码实现
5. **bytes 和 str 的区别？** - bytes 是字节序列，str 是 Unicode 字符串

### 5. 数据结构

> [!TIP] Java 开发者视角
> Python 的数据结构与 Java 有显著差异：
> - **List** ≈ `ArrayList`，但更强大（可存混合类型）
> - **Tuple** ≈ 不可变的 List，Java 无等价类型
> - **Set** ≈ `HashSet`
> - **Dict** ≈ `HashMap`

---

#### 5.1 列表（List）

##### 5.1.1 创建与访问

```python
# 基本创建
empty = []                      # 空列表
numbers = [1, 2, 3, 4, 5]       # 整数列表
mixed = [1, "hello", 3.14, True]  # 混合类型（Python 允许，Java 不允许）

# list() 构造函数
chars = list("hello")           # ['h', 'e', 'l', 'l', 'o']
items = list(range(5))          # [0, 1, 2, 3, 4]
items = list(range(1, 6))      # [1, 2, 3, 4, 5]
items = list(range(0, 10, 2))  # [0, 2, 4, 6, 8]

# 列表乘法（重复）
zeros = [0] * 5                 # [0, 0, 0, 0, 0]
pattern = [1, 2] * 3           # [1, 2, 1, 2, 1, 2]

# 索引访问（0-based）
numbers = [10, 20, 30, 40, 50]
numbers[0]     # 10（第一个）
numbers[4]     # 50（最后一个）
numbers[-1]    # 50（倒数第一）
numbers[-2]    # 40（倒数第二）

# 切片访问
numbers[1:4]   # [20, 30, 40]（start:end，不含 end）
numbers[:3]    # [10, 20, 30]（从头开始）
numbers[3:]     # [40, 50]（到末尾）
numbers[::2]   # [10, 30, 50]（步长 2）
numbers[::-1]   # [50, 40, 30, 20, 10]（反转）
```

> [!WARNING] 列表可变
> 列表是**可变**的，可以直接修改：`numbers[0] = 100`

**Java 对比**：
```java
// Java - 必须声明类型
List<Integer> numbers = new ArrayList<>(Arrays.asList(1, 2, 3));
// 或 Java 9+
List.of(1, 2, 3);  // 不可变
```

##### 5.1.2 增删改查操作

```python
numbers = [1, 2, 3]

# 增 - 在末尾添加
numbers.append(4)      # [1, 2, 3, 4]
numbers.append([5, 6]) # [1, 2, 3, 4, [5, 6]]（整体作为一个元素）

# 增 - 在指定位置插入
numbers.insert(0, 0)   # [0, 1, 2, 3, 4]（在索引 0 插入）
numbers.insert(2, 99)  # [0, 1, 99, 2, 3, 4]

# 增 - 扩展列表
numbers.extend([7, 8])  # [0, 1, 99, 2, 3, 4, 7, 8]
# 区别于 append
[1, 2].append([3, 4])   # [1, 2, [3, 4]]
[1, 2].extend([3, 4])   # [1, 2, 3, 4]

# 删 - 按值删除
numbers.remove(99)      # 删除第一个匹配的值
# numbers.remove(100)   # ValueError: list.remove(x) - 不存在会报错

# 删 - 按索引删除
numbers.pop()           # 删除最后一个，返回被删除的值
numbers.pop(0)          # 删除第一个，返回被删除的值
del numbers[0]          # 删除索引 0 的元素（不返回）

# 删 - 清空
numbers.clear()         # []

# 改
numbers = [1, 2, 3, 4]
numbers[0] = 100        # [100, 2, 3, 4]（按索引修改）
numbers[1:3] = [20, 30] # [100, 20, 30, 4]（切片修改）

# 查
numbers = [1, 2, 3, 4, 3, 3]
numbers.index(3)        # 2（第一个匹配的索引）
numbers.index(3, 4)     # 4（从索引 4 开始查找）
numbers.count(3)        # 3（计数）
3 in numbers            # True（成员判断）
```

##### 5.1.3 列表方法详解

```python
# sort() - 排序（原地修改）
numbers = [3, 1, 4, 1, 5, 9, 2, 6]
numbers.sort()          # [1, 1, 2, 3, 4, 5, 6, 9]
numbers.sort(reverse=True)  # [9, 6, 5, 4, 3, 2, 1, 1]

# 按key排序
words = ["banana", "apple", "cherry"]
words.sort(key=len)    # 按长度排序：['apple', 'banana', 'cherry']
words.sort(key=lambda x: x[-1])  # 按最后一个字母排序

# sorted() - 返回新列表（不修改原列表）
numbers = [3, 1, 4, 1, 5]
sorted(numbers)        # [1, 1, 3, 4, 5]
numbers                 # [3, 1, 4, 1, 5]（原列表不变）

# reverse() - 反转（原地修改）
numbers.reverse()       # [5, 1, 4, 1, 3]
reversed(numbers)       # 返回迭代器，需要 list() 转换

# copy() - 浅拷贝
original = [1, [2, 3], 4]
copied = original.copy()
copied[1].append(99)   # original 也会被修改！（浅拷贝问题）
```

##### 5.1.4 列表推导式（重要！Pythonic）

```python
# 基本语法：[表达式 for item in iterable]
squares = [x ** 2 for x in range(10)]  # [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]

# 带条件：[表达式 for item in iterable if 条件]
evens = [x for x in range(10) if x % 2 == 0]  # [0, 2, 4, 6, 8]

# 多重循环
pairs = [(x, y) for x in [1, 2] for y in [3, 4]]
# [(1, 3), (1, 4), (2, 3), (2, 4)]

# 条件表达式（类似三元运算符）
labels = ["偶数" if x % 2 == 0 else "奇数" for x in range(5)]
# ['偶数', '奇数', '偶数', '奇数', '偶数']

# 嵌套列表推导式
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flattened = [num for row in matrix for num in row]
# [1, 2, 3, 4, 5, 6, 7, 8, 9]

# 字典推导式转列表
word = "hello"
char_count = {c: word.count(c) for c in set(word)}
# {'h': 1, 'e': 1, 'l': 2, 'o': 1}
```

> [!TIP] Agent 开发场景
> 列表推导式是处理 LLM 返回的 JSON 列表的利器：
> ```python
> responses = ["北京", "上海", "广州", "深圳"]
> items = [f"{i+1}. {city}" for i, city in enumerate(responses)]
> # ['1. 北京', '2. 上海', '3. 广州', '4. 深圳']
> ```

##### 5.1.5 列表的"坑"

```python
# 坑1：浅拷贝问题
a = [[1, 2], [3, 4]]
b = a[:]          # 浅拷贝
b[0].append(99)  # a 也会变！
# 正确深拷贝：
import copy
b = copy.deepcopy(a)

# 坑2：列表相乘初始化
zeros = [[0] * 3 for _ in range(3)]  # 正确！每个都是独立列表
wrong = [[0] * 3] * 3                # 错误！所有行指向同一列表

# 坑3：修改列表时的迭代问题
# 不要在遍历列表时直接删除元素
numbers = [1, 2, 2, 3, 2, 4]
# 错误：for num in numbers: if num == 2: numbers.remove(num)
# 正确：
numbers = [x for x in numbers if x != 2]  # [1, 3, 4]
```

---

#### 5.2 元组（Tuple）

##### 5.2.1 创建与访问

```python
# 基本创建
empty = ()                # 空元组
single = (42,)            # 单元素元组（必须加逗号！）
point = (3, 4)            # 二元组
colors = ("red", "green", "blue")

# tuple() 构造函数
chars = tuple("hello")    # ('h', 'e', 'l', 'l', 'o')
items = tuple([1, 2, 3]) # (1, 2, 3)

# 访问（与列表相同）
colors = ("red", "green", "blue")
colors[0]     # 'red'
colors[-1]    # 'blue'
colors[1:3]   # ('green', 'blue')
```

> [!WARNING] 元组不可变
> 元组创建后**不能修改**：
> ```python
> t = (1, 2, 3)
> t[0] = 100  # TypeError!
> ```

##### 5.2.2 不可变性的意义

```python
# 1. 作为字典的键
locations = {
    (35.6762, 139.6503): "Tokyo",
    (40.7128, -74.0060): "New York",
}

# 2. 函数返回多个值（Python 惯用方式）
def get_stats(numbers):
    return (min(numbers), max(numbers), sum(numbers)/len(numbers))

min_val, max_val, avg_val = get_stats([1, 2, 3, 4, 5])

# 3. 格式化字符串（安全）
info = ("Alice", 30, "Engineer")
print("%s, age %d, works as %s" % info)

# 4. 集合的元素（列表不能作为 set 的元素）
valid = {(1, 2), (3, 4), (5, 6)}  # OK
# invalid = {[1, 2], [3, 4]}      # TypeError!
```

##### 5.2.3 解包操作（重要！）

```python
# 基本解包
point = (3, 4, 5)
x, y, z = point  # x=3, y=4, z=5

# * 解包剩余部分
head, *middle, tail = [1, 2, 3, 4, 5]
# head = 1, middle = [2, 3, 4], tail = 5

first, *_, last = [10, 20, 30, 40, 50]
# first = 10, last = 50, _ 丢弃中间值

# 交换变量（无需 temp）
a, b = 1, 2
a, b = b, a  # a=2, b=1

# 函数返回值解包
def get_user():
    return ("Alice", 30, "alice@email.com")

name, age, email = get_user()

# 解包与 * 的组合
records = [("Alice", 30), ("Bob", 25), ("Charlie", 35)]
names, ages = zip(*records)
# names = ('Alice', 'Bob', 'Charlie')
# ages = (30, 25, 35)
```

**Java 对比**：
```java
// Java 没有元组，只能用数组或自定义类
String[] user = {"Alice", "30"};
String name = user[0];
```

##### 5.2.4 命名元组（namedtuple）

```python
from collections import namedtuple

# 定义命名元组类型
Point = namedtuple('Point', ['x', 'y', 'z'])
User = namedtuple('User', 'name age email')  # 空格分隔也可以

# 创建实例
p = Point(1, 2, 3)
u = User("Alice", 30, "alice@email.com")

# 访问方式 1：属性
p.x           # 1
p.y           # 2
u.name        # 'Alice'

# 访问方式 2：索引
p[0]          # 1
u[0]          # 'Alice'

# 解包
x, y, z = p

# 转换为字典
p._asdict()   # {'x': 1, 'y': 2, 'z': 3}

# 修改字段（返回新实例）
p._replace(x=100)  # Point(x=100, y=2, z=3)
```

> [!TIP] namedtuple 适用场景
> 当你需要"轻量级类"且**不可变**时使用：
> - 数据传输对象（DTO）
> - 配置对象
> - 函数多返回值（比普通元组更清晰）

##### 5.2.5 元组 vs 列表

| 特性 | 元组 | 列表 |
|------|------|------|
| 可变性 | 不可变 | 可变 |
| 性能 | 更快、更省内存 | 稍慢 |
| 用途 | 固定数据、函数返回值 | 动态集合 |
| 作为 dict 键 | ✅ 可以 | ❌ 不可以 |
| 作为 set 元素 | ✅ 可以 | ❌ 不可以 |

---

#### 5.3 集合（Set）

##### 5.3.1 创建与特点

```python
# 基本创建
empty = set()             # 空集合（不能用 {}，那是 dict）
fruits = {"apple", "banana", "cherry"}
numbers = {1, 2, 3, 4, 5}

# set() 构造函数
chars = set("hello")      # {'h', 'e', 'l', 'o'}（去重）
items = set([1, 2, 2, 3]) # {1, 2, 3}

# 特点：无序、唯一
s = {3, 1, 2, 3, 1, 2}
print(s)  # {1, 2, 3}（顺序不确定，但去重）
```

> [!WARNING] 空集合
> `{}` 是空字典，不是空集合。创建空集合必须用 `set()`。

**Java 对比**：
```java
// Java
Set<String> fruits = new HashSet<>(Arrays.asList("apple", "banana"));
```

##### 5.3.2 集合运算

```python
A = {1, 2, 3, 4}
B = {3, 4, 5, 6}

# 并集
A | B          # {1, 2, 3, 4, 5, 6}
A.union(B)     # 同上
A |= B         # 就地修改 A

# 交集
A & B          # {3, 4}
A.intersection(B)  # 同上
A &= B         # 就地修改 A

# 差集（A 有 B 没有）
A - B          # {1, 2}
A.difference(B)   # 同上
A -= B         # 就地修改 A

# 对称差（AB 互斥的部分）
A ^ B          # {1, 2, 5, 6}
A.symmetric_difference(B)  # 同上
A ^= B         # 就地修改 A

# 子集判断
{1, 2} <= {1, 2, 3}   # True（子集）
{1, 2} < {1, 2, 3}    # True（真子集）
{1, 2, 3} >= {1, 2}   # True（超集）
{1, 2, 3} > {1, 2}    # True（真超集）

# 不相交
{1, 2}.isdisjoint({3, 4})  # True
{1, 2}.isdisjoint({2, 3})  # False
```

##### 5.3.3 集合方法

```python
s = {1, 2, 3}

# 增
s.add(4)       # {1, 2, 3, 4}
s.update([5, 6])  # {1, 2, 3, 4, 5, 6}（批量添加）

# 删
s.remove(3)    # {1, 2, 4}（不存在会报错 KeyError）
s.discard(10)  # {}（不存在不会报错）
s.pop()        # 随机删除一个元素并返回

# 查（成员判断）
3 in s         # True（主要用途）

# 其他
len(s)         # 3
s.copy()       # 浅拷贝
s.clear()      # set()
```

##### 5.3.4 集合推导式

```python
# 基本语法：{表达式 for item in iterable}
squares = {x ** 2 for x in range(6)}  # {0, 1, 4, 9, 16, 25}

# 带条件
evens = {x for x in range(10) if x % 2 == 0}  # {0, 2, 4, 6, 8}

# 交集推导式
a = {1, 2, 3, 4}
b = {3, 4, 5, 6}
common = {x for x in a if x in b}  # {3, 4}
```

##### 5.3.5 集合的"坑"

```python
# 坑1：集合元素必须是可哈希的（不可变）
# OK
{1, "hello", (1, 2)}      # 可以
# Error
{{1, 2}, {3, 4}}          # TypeError: unhashable type 'set'
{[1, 2], [3, 4]}          # TypeError: unhashable type 'list'

# 坑2：集合随机删除
s = {1, 2, 3, 4, 5}
s.pop()   # 不知道删除哪个！生产代码避免用 pop()
```

> [!TIP] Agent 开发场景
> 集合用于去重和成员判断：
> ```python
> # 去除重复的 LLM 输出
> responses = ["苹果", "香蕉", "苹果", "橙子", "香蕉"]
> unique = list(set(responses))  # ['苹果', '香蕉', '橙子']
> ```

---

#### 5.4 字典（Dict）

##### 5.4.1 创建与访问

```python
# 基本创建
empty = {}                # 空字典
user = {"name": "Alice", "age": 30}
config = {"theme": "dark", "lang": "zh"}

# dict() 构造函数
pairs = [("a", 1), ("b", 2)]
d = dict(pairs)           # {'a': 1, 'b': 2}

# 关键字参数
d = dict(name="Alice", age=30)  # {'name': 'Alice', 'age': 30}

# fromkeys - 批量创建（值相同）
keys = ["a", "b", "c"]
d = dict.fromkeys(keys, 0)  # {'a': 0, 'b': 0, 'c': 0}

# 访问（键不存在会报错）
user = {"name": "Alice", "age": 30}
user["name"]          # 'Alice'
user["age"]           # 30
# user["email"]        # KeyError

# 安全访问
user.get("name")       # 'Alice'
user.get("email")      # None（不报错）
user.get("email", "N/A")  # 'N/A'（默认值）
```

> [!WARNING] 字典键的要求
> 键必须是**可哈希**的（不可变类型）：
> - ✅ `str`, `int`, `float`, `tuple`, `bytes`
> - ❌ `list`, `dict`, `set`

**Java 对比**：
```java
// Java
Map<String, Object> user = new HashMap<>();
user.put("name", "Alice");
user.get("name");  // 返回 Object，需强转
```

##### 5.4.2 增删改查操作

```python
user = {"name": "Alice", "age": 30}

# 增/改
user["email"] = "alice@email.com"  # 新增
user["age"] = 31                    # 修改

# 批量更新
user.update({"city": "Beijing", "age": 32})
# 相同键会覆盖：user = {"name": "Alice", "age": 32, "email": "alice@email.com", "city": "Beijing"}

# 删
del user["email"]          # 删除指定键
user.pop("age")            # 删除并返回值
user.popitem()             # 删除最后一个（Python 3.7+）
user.clear()               # 清空

# 查
"name" in user            # True（键存在判断）
user.keys()               # dict_keys(['name', 'city'])
user.values()             # dict_values(['Alice', 'Beijing'])
user.items()              # dict_items([('name', 'Alice'), ('city', 'Beijing')])

# 遍历
for key in user:
    print(key, user[key])

for key, value in user.items():
    print(f"{key}: {value}")
```

##### 5.4.3 字典方法详解

```python
# setdefault - 只在键不存在时设置
user = {"name": "Alice"}
user.setdefault("age", 25)    # 25（新增）
user.setdefault("name", "Bob") # 'Alice'（已存在，返回原值）

# 复制
user_copy = user.copy()       # 浅拷贝
import copy
user_deep = copy.deepcopy(user)  # 深拷贝

# 键值迭代顺序（Python 3.7+ 保证插入顺序）
d = {}
d["z"] = 1
d["a"] = 2
d["m"] = 3
print(list(d.keys()))  # ['z', 'a', 'm']（按插入顺序）
```

##### 5.4.4 字典推导式

```python
# 基本语法：{key: value for item in iterable}
squares = {x: x**2 for x in range(5)}  # {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}

# 带条件
nums = [1, 2, 3, 4, 5]
even_squares = {x: x**2 for x in nums if x % 2 == 0}  # {2: 4, 4: 16}

# 键值互换
original = {"a": 1, "b": 2, "c": 3}
inverted = {v: k for k, v in original.items()}  # {1: 'a', 2: 'b', 3: 'c'}

# 合并两个列表
keys = ["name", "age", "city"]
values = ["Alice", 30, "Beijing"]
data = {k: v for k, v in zip(keys, values)}  # {'name': 'Alice', 'age': 30, 'city': 'Beijing'}
```

> [!TIP] Agent 开发场景
> 字典是处理 JSON 的核心：
> ```python
> # LLM 返回的 JSON
> response = {"content": "The capital of France is Paris.", "tokens": 15}
> 
> # 构建 prompt 变量
> prompt_vars = {
>     "user_name": "Alice",
>     "response": response["content"],
>     "tokens": response.get("tokens", 0)
> }
> ```

##### 5.4.5 嵌套字典

```python
# 嵌套结构
company = {
    "name": "TechCorp",
    "departments": {
        "engineering": {
            "headcount": 50,
            "members": ["Alice", "Bob"]
        },
        "sales": {
            "headcount": 20,
            "members": ["Charlie", "David"]
        }
    }
}

# 访问嵌套值
company["departments"]["engineering"]["headcount"]  # 50

# 安全访问（链式 get）
company.get("departments", {}).get("engineering", {}).get("headcount", 0)

# 使用 setdefault 安全添加
company.setdefault("departments", {}).setdefault("hr", {"headcount": 10})
```

##### 5.4.6 defaultdict（更安全的字典）

```python
from collections import defaultdict

# 普通字典的坑
# counts = {}
# for word in ["apple", "banana", "apple"]:
#     counts[word] += 1  # KeyError!

# defaultdict 解决方案
counts = defaultdict(int)  # 默认值为 0
for word in ["apple", "banana", "apple"]:
    counts[word] += 1
# counts = {'apple': 2, 'banana': 1}

# 其他默认值类型
dd_list = defaultdict(list)
dd_list["fruits"].append("apple")  # {'fruits': ['apple']}

dd_set = defaultdict(set)
dd_set["evens"].add(2)  # {'evens': {2}}

# 复杂结构
tree = defaultdict(lambda: defaultdict(int))
tree["2024"]["sales"] += 100
```

##### 5.4.7 字典的"坑"

```python
# 坑1：字典键大小写敏感
d = {"Name": "Alice"}
d["name"]   # KeyError！（大小写不同）

# 坑2：修改字典时不要修改大小
d = {1: "a", 2: "b"}
for key in d:
    if key == 1:
        del d[key]  # RuntimeError: dictionary changed size during iteration

# 正确做法
to_delete = [k for k in d if k == 1]
for k in to_delete:
    del d[k]

# 坑3：字典比较（值比较，非键值比较）
{"a": 1} == {"a": 1}   # True
{"a": 1} == {"b": 1}   # False（键不同）
```

---

#### 📋 数据结构对比速查表

| 操作 | List | Tuple | Set | Dict |
|------|------|-------|-----|------|
| 创建 | `[1,2]` / `list()` | `(1,2)` / `tuple()` | `{1,2}` / `set()` | `{"a":1}` / `dict()` |
| 可变 | ✅ | ❌ | ✅ | ✅ |
| 有序 | ✅ (3.7+) | ✅ | ❌ | ✅ (3.7+) |
| 索引访问 | ✅ | ✅ | ❌ | ✅ by key |
| 去重 | ❌ | ❌ | ✅ | ❌ |
| 作为键 | ❌ | ✅ | ❌ | ❌ |
| 作为元素 | ✅ | ✅ | ❌ (可哈希) | ❌ |

---

#### 🎯 面试高频考点

1. **Python 列表和元组的区别？** - 列表可变、元组不可变（决定用途）
2. **浅拷贝 vs 深拷贝？** - 浅拷贝只拷贝引用，深拷贝递归拷贝所有层级
3. **字典的键有什么限制？** - 必须可哈希（不可变类型）
4. **Python 3.7+ 字典有什么特性？** - 保持插入顺序
5. **什么时候用 set 而不是 list？** - 需要去重或快速成员判断时（O(1) vs O(n)）
6. **什么是 defaultdict？** - 提供默认值的字典，避免 KeyError

### 6. 流程控制

> [!TIP] Java 开发者视角
> Python 的流程控制与 Java 类似，但语法更简洁：
> - 没有 `switch`，用 `elif` 链替代
> - `for` 循环是 `for-each` 风格（迭代器）
> - 有独特的 `else` 子句（循环正常结束时执行）

---

#### 6.1 条件语句

##### 6.1.1 if 语句

```python
# 基本语法（注意缩进！）
age = 18
if age >= 18:
    print("成年人")  # 4空格缩进

# 多行条件
if age >= 18 and age < 65:
    print("劳动年龄")
```

**Java 对比**：
```java
// Java - 用大括号
if (age >= 18) {
    System.out.println("成年人");
}
```

##### 6.1.2 if-else 语句

```python
age = 16

if age >= 18:
    print("成年人")
else:
    print("未成年")

# 单行 if-else（表达式形式）
status = "成年人" if age >= 18 else "未成年"
```

> [!TIP] Python 没有三元运算符 `? :`
> Python 用 `if-else` 表达式替代：
> ```python
> # Java: String status = age >= 18 ? "成年人" : "未成年";
> # Python:
> status = "成年人" if age >= 18 else "未成年"
> ```

##### 6.1.3 if-elif-else 链

```python
score = 85

if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
elif score >= 60:
    grade = "D"
else:
    grade = "F"

# 可以只有一个 if
if score >= 90:
    grade = "A"
```

> [!WARNING] Python 没有 switch
> Java 的 `switch` 在 Python 中用 `elif` 链替代。

##### 6.1.4 条件表达式（Expression vs Statement）

```python
# if-else 是语句（不返回值）
if x > 0:
    sign = "positive"
else:
    sign =non-positive"

# 条件表达式是表达式（返回值）
sign = "positive" if x > 0 else "non-positive"

# 嵌套条件表达式（谨慎使用）
age_group = (
    "儿童" if age < 12 else
    "青少年" if age < 18 else
    "成年人" if age < 65 else
    "老年人"
)
```

##### 6.1.5 短路求值

```python
# and 短路
result = False and something()  # something() 不执行
# or 短路
result = True or something()    # something() 不执行

# 常见用法：默认值
name = user_input or "Anonymous"
```

##### 6.1.6 条件判断的真假值

```python
# Falsy 值（判断为 False）
bool(None)      # False
bool(0)         # False
bool("")        # False
bool([])        # False
bool({})        # False
bool(set())     # False

# Truthy 值（其他）
bool("hello")   # True
bool([0])       # True（即使列表只有一个0）
bool({"a": 1})  # True

# 面试题：[] == False ?
[] == False     # False！（不是 False）
not []          # True（但这是 not，不是 ==）
```

---

#### 6.2 循环语句

##### 6.2.1 while 循环

```python
# 基本语法
count = 0
while count < 5:
    print(count)
    count += 1

# while-else（循环正常结束时执行 else）
count = 0
while count < 3:
    print(count)
    count += 1
else:
    print("循环正常结束")  # count == 3 时执行

# break 退出时不执行 else
count = 0
while count < 3:
    if count == 2:
        break
    count += 1
else:
    print("不会执行")
```

> [!WARNING] 死循环
> ```python
> # 常见错误：忘记更新条件
> while True:  # 死循环！
>     print("会一直执行")
> ```

##### 6.2.2 for 循环（迭代器）

```python
# 基本语法：for item in iterable
fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    print(fruit)

# Java 的增强 for 循环类似
# Java: for (String fruit : fruits) { System.out.println(fruit); }
```

**Python for vs Java for**：
```java
// Java - 两种 for
for (int i = 0; i < 5; i++) { ... }  // 传统索引循环
for (String item : list) { ... }      // for-each

// Python - 统一用迭代器
for i in range(5): ...                 # 替代索引循环
for item in items: ...                 # 等同于 for-each
```

##### 6.2.3 range() 函数

```python
# range(stop) - 从 0 开始
list(range(5))        # [0, 1, 2, 3, 4]

# range(start, stop)
list(range(1, 6))     # [1, 2, 3, 4, 5]

# range(start, stop, step)
list(range(0, 10, 2)) # [0, 2, 4, 6, 8]
list(range(10, 0, -1)) # [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]

# 正序
for i in range(5):
    print(i)  # 0, 1, 2, 3, 4

# 逆序
for i in range(4, -1, -1):
    print(i)  # 4, 3, 2, 1, 0
```

> [!TIP] range 内存效率
> `range(1000000)` 不会生成一百万个数字，而是返回一个惰性迭代器，占用很少内存。

##### 6.2.4 break、continue、pass

```python
# break - 跳出整个循环
for i in range(10):
    if i == 5:
        break
    print(i)  # 0, 1, 2, 3, 4

# continue - 跳过本次迭代
for i in range(5):
    if i == 2:
        continue
    print(i)  # 0, 1, 3, 4（跳过2）

# pass - 占位符（什么都不做）
for i in range(5):
    if i == 2:
        pass  # TODO: 以后处理
    else:
        print(i)
```

> [!WARNING] pass vs continue
> `pass` 什么都不做，继续执行；`continue` 跳过本次循环剩余代码：
> ```python
> # pass - 打印所有数字
> for i in range(3):
>     if i == 1:
>         pass
>     print(i)  # 0, 1, 2
>
> # continue - 跳过1
> for i in range(3):
>     if i == 1:
>         continue
>     print(i)  # 0, 2
> ```

##### 6.2.5 循环的 else 子句（Python 独有！）

```python
# else 在循环正常结束时执行
for i in range(3):
    print(i)
else:
    print("循环完成")  # 执行

# break 退出时不执行 else
for i in range(3):
    if i == 1:
        break
    print(i)
else:
    print("不会执行")  # 不执行

# 典型用法：查找
numbers = [1, 3, 5, 7]
target = 6

for n in numbers:
    if n == target:
        print(f"找到 {target}")
        break
else:
    print(f"未找到 {target}")  # 循环正常结束才执行
```

> [!TIP] else 的语义
> Python 的循环 else 可以理解为 "nobreak"——当循环**没有**被 break 退出时执行。

##### 6.2.6 循环嵌套

```python
# 打印九九乘法表
for i in range(1, 10):
    for j in range(1, i + 1):
        print(f"{j}×{i}={i*j}", end="\t")
    print()  # 换行

# 跳出多层循环（Python 没有 label）
for i in range(5):
    for j in range(5):
        if j == 3:
            break  # 只跳出内层
        print(i, j)
```

**Java 对比**：
```java
// Java 可以用 label 跳出多层循环
outer:
for (int i = 0; i < 5; i++) {
    for (int j = 0; j < 5; j++) {
        if (j == 3) break outer;  // 跳出两层
    }
}

// Python 只能 break 一层，或用异常/标志位
```

##### 6.2.7 enumerate - 带索引的迭代

```python
fruits = ["apple", "banana", "cherry"]

# 方法1：手动索引
for i in range(len(fruits)):
    print(f"{i}: {fruits[i]}")

# 方法2：enumerate（推荐）
for i, fruit in enumerate(fruits, start=1):
    print(f"{i}: {fruit}")
# 1: apple
# 2: banana
# 3: cherry
```

##### 6.2.8 zip - 并行迭代

```python
names = ["Alice", "Bob", "Charlie"]
ages = [30, 25, 35]

# 并行遍历
for name, age in zip(names, ages):
    print(f"{name}: {age}")
# Alice: 30
# Bob: 25
# Charlie: 35

# 不等长时取最短
names = ["Alice", "Bob"]
ages = [30, 25, 35, 40]
for name, age in zip(names, ages):
    print(f"{name}: {age}")  # 只迭代到最短长度

# 最短长度后继续（Python 3.10+）
for name, age in itertools.zip_longest(names, ages, fillvalue="未知"):
    print(f"{name}: {age}")
```

##### 6.2.9 列表推导式中的 if

```python
# 带条件的列表推导式
evens = [x for x in range(10) if x % 2 == 0]
# [0, 2, 4, 6, 8]

# if-else 表达式（放前面）
labels = ["偶数" if x % 2 == 0 else "奇数" for x in range(5)]
# ['偶数', '奇数', '偶数', '奇数', '偶数']
```

##### 6.2.10 循环性能技巧

```python
# ❌ 慢：在循环中拼接字符串
result = ""
for i in range(1000):
    result += str(i)

# ✅ 快：使用 join
parts = []
for i in range(1000):
    parts.append(str(i))
result = "".join(parts)

# ✅ 最快：列表推导式
result = "".join(str(i) for i in range(1000))

# ❌ 慢：重复访问长度
for i in range(len(items)):
    if i < len(items):  # 每次都计算

# ✅ 快：缓存长度
n = len(items)
for i in range(n):
    if i < n:  # 使用缓存值
```

---

#### 6.3 迭代工具实战

##### 6.3.1 itertools 模块

```python
import itertools

# cycle - 无限循环
counter = 0
for item in itertools.cycle(["a", "b", "c"]):
    print(item)
    counter += 1
    if counter == 5:  # 手动停止
        break
# a, b, c, a, b

# count - 无限计数
for i in itertools.count(start=0, step=2):
    print(i)
    if i > 10:
        break
# 0, 2, 4, 6, 8, 10, 12

# chain - 连接多个迭代器
for item in itertools.chain([1, 2], ["a", "b"], [3, 4]):
    print(item)
# 1, 2, a, b, 3, 4

# islice - 切片迭代器
for item in itertools.islice(range(10), 2, 8, 2):
    print(item)
# 2, 4, 6
```

##### 6.3.2 生成器表达式（惰性求值）

```python
# 列表推导式（立即求值）
squares = [x**2 for x in range(1000000)]  # 立即占用大量内存

# 生成器表达式（惰性求值）
squares_gen = (x**2 for x in range(1000000))  # 占用很少内存
for sq in squares_gen:
    print(sq)
    if sq > 100:
        break
```

---

#### 📋 流程控制速查表

| 关键字 | 作用 |
|--------|------|
| `if/elif/else` | 条件分支 |
| `for` | 迭代循环 |
| `while` | 条件循环 |
| `break` | 跳出当前循环 |
| `continue` | 跳过本次迭代 |
| `pass` | 空操作占位符 |
| `else` (循环后) | 循环正常结束时执行 |

---

#### 🎯 面试高频考点

1. **Python 的 `for` 和 Java 的 `for` 有什么区别？**
   - Python 的 `for` 是 for-each，Java 有两种
   - Python 用 `range()` 模拟索引循环

2. **Python 有没有 switch？**
   - 没有，用 `elif` 链替代

3. **循环的 `else` 什么时候执行？**
   - 循环正常结束（没有被 break）时执行

4. **什么是短路求值？**
   - `and`/`or` 在能确定结果时不再计算右侧表达式

5. **Falsy 值有哪些？**
   - `None`, `0`, `""`, `[]`, `{}`, `set()`

6. **`pass` 和 `continue` 的区别？**
   - `pass` 什么都不做，继续执行下一行
   - `continue` 跳过本次循环剩余代码

---

### 7. 函数基础

> [!TIP] Java 开发者视角
> Python 函数与 Java 方法的主要区别：
> - Python 函数是**一等公民**（可以赋值给变量、作为参数传递）
> - 没有 `void` 关键字，用 `return None` 表示无返回值
> - 不需要声明返回类型（可用 Type Hints 标注）
> - 参数传递类似**按对象引用传递**（类似 Java 的引用传递）

---

#### 7.1 函数定义与调用

##### 7.1.1 基本语法

```python
# 无参数函数
def greet():
    print("Hello, World!")

greet()  # 调用

# 有参数函数
def greet(name):
    print(f"Hello, {name}!")

greet("Alice")  # Hello, Alice!

# 有返回值的函数
def add(a, b):
    return a + b

result = add(1, 2)  # 3
```

> [!WARNING] Python 函数不标注返回类型
> 虽然可以加 Type Hints，但运行时不强制检查：
> ```python
> def add(a: int, b: int) -> int:
>     return a + b
> # 仍然可以返回字符串，不会报错
> ```

**Java 对比**：
```java
// Java 方法
public int add(int a, int b) {
    return a + b;
}
```

##### 7.1.2 函数是第一等公民

```python
# 函数可以赋值给变量
def square(x):
    return x ** 2

f = square  # f 现在是 square 函数
print(f(5))  # 25

# 函数可以作为参数传递
def apply(func, value):
    return func(value)

result = apply(square, 5)  # 25

# 函数可以作为返回值
def multiplier(n):
    def multiply(x):
        return x * n
    return multiply

double = multiplier(2)
print(double(5))  # 10
```

> [!TIP] 一等公民的意义
> 这使得 Python 支持**函数式编程**范式：map、filter、reduce、装饰器等

##### 7.1.3 文档字符串（Docstring）

```python
def calculate_area(width, height):
    """计算矩形面积。
    
    Args:
        width: 宽度（单位：米）
        height: 高度（单位：米）
    
    Returns:
        矩形面积（单位：平方米）
    """
    return width * height

# 访问 docstring
print(calculate_area.__doc__)
help(calculate_area)
```

> [!TIP] Docstring 是 Agent 开发的核心
> Agent 工具的描述、参数说明都来源于此。格式推荐 Google Style 或 NumPy Style。

---

#### 7.2 参数传递

##### 7.2.1 位置参数

```python
# 按位置传递（与 Java 相同）
def power(base, exponent):
    return base ** exponent

power(2, 3)   # 8
power(3, 2)   # 9
```

##### 7.2.2 关键字参数

```python
# 按名称传递
def greet(name, age):
    print(f"{name}, {age}岁")

greet(age=30, name="Alice")  # 顺序可以不同
```

**Java 对比**：
```java
// Java 没有关键字参数，只能按位置
greet("Alice", 30);
```

##### 7.2.3 默认参数

```python
# 默认参数
def greet(name, greeting="Hello"):
    print(f"{greeting}, {name}!")

greet("Alice")              # Hello, Alice!
greet("Bob", "Hi")          # Hi, Bob!
```

> [!WARNING] 默认参数必须是不可变对象
> 常见错误：使用列表或字典作为默认参数
> ```python
> # ❌ 错误！默认参数在定义时求值，只求值一次
> def add_item(item, items=[]):
>     items.append(item)
>     return items
> 
> add_item(1)  # [1]
> add_item(2)  # [1, 2]  期望是 [2]！
> 
> # ✅ 正确写法
> def add_item(item, items=None):
>     if items is None:
>         items = []
>     items.append(item)
>     return items
> ```

##### 7.2.4 可变位置参数（*args）

```python
# *args 接收任意数量的位置参数（打包为元组）
def sum(*numbers):
    total = 0
    for n in numbers:
        total += n
    return total

sum(1, 2, 3)       # 6
sum(1, 2, 3, 4, 5)  # 15

# 解包操作
numbers = [1, 2, 3, 4]
sum(*numbers)     # 10（把列表展开为位置参数）
```

##### 7.2.5 可变关键字参数（**kwargs）

```python
# **kwargs 接收任意数量的关键字参数（打包为字典）
def print_info(**info):
    for key, value in info.items():
        print(f"{key}: {value}")

print_info(name="Alice", age=30, city="Beijing")
# name: Alice
# age: 30
# city: Beijing

# 解包操作
data = {"name": "Bob", "age": 25}
print_info(**data)  # 展开字典为关键字参数
```

##### 7.2.6 参数组合

```python
# 组合使用（顺序固定）
def func(pos1, pos2, *args, key1="default", **kwargs):
    print(f"pos: {pos1}, {pos2}")
    print(f"args: {args}")
    print(f"key1: {key1}")
    print(f"kwargs: {kwargs}")

func(1, 2, 3, 4, key1="custom", name="Alice")
# pos: 1, 2
# args: (3, 4)
# key1: custom
# kwargs: {'name': 'Alice'}
```

> [!TIP] 强制关键字参数（Python 3）
> ```python
> def func(pos_only, *, kw_only1, kw_only2):
>     # * 之后的参数必须用关键字传递
>     pass
> 
> func(1, kw_only1=2, kw_only2=3)  # OK
> func(1, 2, 3)  # TypeError!
> ```

---

#### 7.3 返回值与多返回值

##### 7.3.1 基本返回值

```python
# 无 return 或 return None
def no_return():
    print("Hello")

result = no_return()  # None

# 单返回值
def get_name():
    return "Alice"

name = get_name()  # "Alice"
```

##### 7.3.2 多返回值（Python 特有！）

```python
# 返回元组
def get_stats(numbers):
    return min(numbers), max(numbers), sum(numbers) / len(numbers)

# 解包
min_val, max_val, avg_val = get_stats([1, 2, 3, 4, 5])
# min_val = 1, max_val = 5, avg_val = 3.0

# 整体接收
result = get_stats([1, 2, 3])
# result = (1, 5, 3.0)
```

**Java 对比**：
```java
// Java 没有多返回值，必须用数组/对象/包装
public class Stats {
    public int min;
    public int max;
    public double avg;
}

// 或返回数组
public int[] getStats(List<Integer> numbers) {
    return new int[]{min, max, avg};
}
```

##### 7.3.3 早期返回（Guard Clauses）

```python
# 防御式编程：提前返回减少嵌套
def process(user):
    # ❌ 嵌套写法
    if user is not None:
        if user.is_active:
            if user.has_permission:
                # 执行逻辑
                pass
    
    # ✅ 卫语句写法（Guard Clauses）
    if user is None:
        return None
    if not user.is_active:
        return None
    if not user.has_permission:
        return None
    
    # 执行逻辑
    return process_successfully(user)
```

---

#### 7.4 变量作用域

##### 7.4.1 LEGB 规则

Python 按以下顺序查找变量：

```
L - Local      函数内部
E - Enclosing   闭包函数（外层函数）
G - Global      模块（文件）级别
B - Built-in    Python 内置（len, print 等）
```

```python
x = "global"  # Global

def outer():
    x = "enclosing"  # Enclosing
    
    def inner():
        x = "local"  # Local
        print(x)     # "local"（先找 local）
    
    inner()
    print(x)          # "enclosing"

outer()
print(x)              # "global"
```

##### 7.4.2 global 和 nonlocal

```python
# global - 声明使用全局变量
counter = 0

def increment():
    global counter
    counter += 1

increment()
print(counter)  # 1
```

> [!WARNING] 滥用全局变量
> 全局变量使代码难以调试和维护。优先使用参数传递和返回值。

```python
# nonlocal - 声明使用闭包外层变量
def outer():
    x = "outer"
    
    def inner():
        nonlocal x
        x = "inner"
        print(x)
    
    inner()
    print(x)

outer()  # "inner", "inner"
```

##### 7.4.3 闭包（Closure）

```python
# 闭包：内层函数记住外层函数的变量
def make_multiplier(factor):
    def multiply(number):
        return number * factor
    return multiply

times_3 = make_multiplier(3)
times_5 = make_multiplier(5)

print(times_3(10))  # 30
print(times_5(10))  # 50
```

> [!TIP] 闭包 vs lambda
> 闭包是带状态的函数，比 lambda 更强大：
> ```python
> # lambda 闭包
> def make_multiplier(factor):
>     return lambda n: n * factor
> ```

---

#### 7.5 递归函数

##### 7.5.1 基本递归

```python
# 阶乘
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)

factorial(5)  # 120

# 斐波那契数列
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

fibonacci(10)  # 55
```

> [!WARNING] 递归深度限制
> Python 默认递归深度约 1000，超过会 `RecursionError`：
> ```python
> import sys
> sys.getrecursionlimit()  # 1000
> sys.setrecursionlimit(2000)  # 可以调整，但不推荐
> ```

##### 7.5.2 尾递归优化

```python
# Python 不支持尾递归优化（不同于 Scheme/Haskell）
# 但可以用迭代替代

# ❌ 递归（栈溢出风险）
def fibonacci(n, a=0, b=1):
    if n == 0:
        return a
    return fibonacci(n - 1, b, a + b)

# ✅ 迭代（推荐）
def fibonacci_iter(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a
```

##### 7.5.3 递归的常见模式

```python
# 1. 树结构遍历
class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def inorder(node):
    if node is None:
        return []
    return inorder(node.left) + [node.val] + inorder(node.right)

# 2. 分治法
def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + middle + quicksort(right)
```

---

#### 7.6 lambda 表达式

##### 7.6.1 基本语法

```python
# lambda 参数: 表达式
square = lambda x: x ** 2
add = lambda x, y: x + y

square(5)  # 25
add(1, 2)  # 3

# 等同于
def square(x):
    return x ** 2
```

> [!WARNING] lambda 的限制
> lambda 只能是**单个表达式**，不能包含语句（if、for、while 等）。

##### 7.6.2 常见用法

```python
# 配合高阶函数
numbers = [3, 1, 4, 1, 5, 9, 2, 6]
sorted(numbers, key=lambda x: -x)  # 降序排列

# map - 对每个元素应用函数
list(map(lambda x: x * 2, [1, 2, 3]))  # [2, 4, 6]

# filter - 过滤元素
list(filter(lambda x: x % 2 == 0, [1, 2, 3, 4]))  # [2, 4]

# reduce - 累积计算
from functools import reduce
reduce(lambda x, y: x + y, [1, 2, 3, 4])  # 10
```

**Java 对比**：
```java
// Java 使用匿名内部类或 Lambda (Java 8+)
// Python lambda ≈ Java 的 Lambda 表达式
// Python 的 map/filter ≈ Java Stream API
```

##### 7.6.3 lambda vs 普通函数

| 特性 | lambda | def 函数 |
|------|--------|---------|
| 语句 | ❌ 只能是表达式 | ✅ 可以有多种语句 |
| 名称 | 匿名 | 有名称 |
| 文档 | ❌ 无法添加 | ✅ 可以有 docstring |
| 作用域 | 受限 | 完全 |
| 复杂度 | 简单 | 任意复杂 |
| 使用场景 | 短函数、高阶函数参数 | 复杂逻辑 |

> [!TIP] 何时用 lambda
> - 作为参数传递给 `map`、`filter`、`sorted`
> - 定义简单的、一次性的函数
> - 闭包中捕获变量
>
> **何时不用**：逻辑复杂、多次使用、需要文档

---

#### 7.7 装饰器（Decorator）

##### 7.7.1 基本概念

```python
# 装饰器：包装函数，增强功能
def my_decorator(func):
    def wrapper(*args, **kwargs):
        print("Before calling")
        result = func(*args, **kwargs)
        print("After calling")
        return result
    return wrapper

@my_decorator
def say_hello():
    print("Hello!")

say_hello()
# Before calling
# Hello!
# After calling
```

**等同于**：
```python
def say_hello():
    print("Hello!")

say_hello = my_decorator(say_hello)
```

##### 7.7.2 常用装饰器

```python
# 计时装饰器
import time
from functools import wraps

def timer(func):
    @wraps(func)  # 保留原函数元信息
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print(f"{func.__name__} took {time.time() - start:.2f}s")
        return result
    return wrapper

@timer
def slow_function():
    time.sleep(1)
    return "Done"

# 类作为装饰器
class CallCounter:
    def __init__(self, func):
        self.count = 0
        self.func = func
    
    def __call__(self, *args, **kwargs):
        self.count += 1
        print(f"{self.func.__name__} called {self.count} times")
        return self.func(*args, **kwargs)

@CallCounter
def greet():
    print("Hello!")
```

---

#### 📋 函数速查表

| 特性 | 语法 | 说明 |
|------|------|------|
| 基本函数 | `def f(x): return x**2` | |
| 默认参数 | `def f(x=1):` | 不可变对象 |
| 可变参数 | `def f(*args):` | 元组 |
| 关键字参数 | `def f(**kwargs):` | 字典 |
| lambda | `lambda x: x**2` | 单表达式 |
| 装饰器 | `@decorator` | 函数包装 |

---

#### 🎯 面试高频考点

1. **Python 函数参数传递是值传递还是引用传递？**
   - 类似"按对象引用传递"（Object Reference），相当于 Java 的引用传递

2. **什么是闭包？**
   - 内层函数记住外层函数的变量

3. **默认参数为什么不能用可变对象？**
   - 默认参数在函数定义时求值，只求值一次，可变对象会被共享

4. **lambda 和普通函数的区别？**
   - lambda 是单表达式匿名函数，不能包含语句

5. **LEGB 是什么？**
   - Local → Enclosing → Global → Built-in 变量查找顺序

6. **装饰器的作用？**
   - 增强函数功能，不修改原函数代码

---

#### 🔬 深入理解：类、对象、函数、方法、构造体区别

##### 7.8.1 核心概念辨析

```python
# 1. 类（Class）- 蓝图/模板
class Dog:
    """Dog 类定义"""
    species = "犬科"  # 类属性
    
    def __init__(self, name, age):  # 构造函数
        self.name = name  # 实例属性
        self.age = age
    
    def bark(self):  # 实例方法
        return f"{self.name} 在叫！"

# 2. 对象（Object）- 类的实例
dog1 = Dog("旺财", 3)  # dog1 是 Dog 类的实例
dog2 = Dog("小白", 5)  # dog2 是另一个实例

# 3. 函数（Function）- 独立函数
def standalone_function(x):
    """独立函数，不属于任何类"""
    return x * 2

# 4. 方法（Method）- 绑定到类/对象的函数
#    - 实例方法：第一个参数是 self
#    - 类方法：第一个参数是 cls
#    - 静态方法：没有 self/cls
```

##### 7.8.2 方法 vs 函数

| 特性 | 方法 (Method) | 函数 (Function) |
|------|--------------|-----------------|
| 归属 | 属于类或对象 | 独立存在 |
| 调用方式 | `obj.method()` 或 `cls.method()` | `function()` |
| 第一个参数 | `self` 或 `cls`（自动绑定） | 需要显式传递 |
| 定义位置 | 类内部 | 类外部（模块级别） |
| 访问权限 | 可访问实例/类属性 | 不能直接访问实例属性 |

```python
class MyClass:
    def instance_method(self):  # 隐式接收 self
        return "instance"
    
    @classmethod
    def class_method(cls):     # 隐式接收 cls
        return "class"
    
    @staticmethod
    def static_method():       # 无隐式参数
        return "static"

# 调用
obj = MyClass()
obj.instance_method()   # 需要实例
MyClass.class_method() # 不需要实例
MyClass.static_method() # 不需要实例
```

##### 7.8.3 实例方法、类方法、静态方法对比

```python
class Circle:
    pi = 3.14159  # 类属性
    
    def __init__(self, radius):
        self.radius = radius  # 实例属性
    
    # 实例方法：可以访问实例和类属性
    def area(self):
        return Circle.pi * self.radius ** 2
    
    # 类方法：可以访问类属性，不能访问实例属性
    @classmethod
    def from_diameter(cls, diameter):
        return cls(diameter / 2)
    
    # 静态方法：与类无关的纯函数
    @staticmethod
    def is_valid_radius(radius):
        return radius > 0

# 使用
c = Circle(5)
c.area()                    # 78.54
Circle.from_diameter(10)   # Circle(radius=5)
Circle.is_valid_radius(5) # True
```

##### 7.8.4 callable 对象

```python
# 任何可以像函数一样调用的都是 callable
# 函数是 callable
# 类也是 callable（调用创建实例）
class Adder:
    def __init__(self, n):
        self.n = n
    
    def __call__(self, x):
        """使对象可以像函数一样调用"""
        return self.n + x

add_5 = Adder(5)
add_5(10)  # 15（像函数一样调用）
isinstance(add_5, Callable)  # True
```

##### 7.8.5 数据类 vs 普通类

```python
from dataclasses import dataclass
from typing import List

@dataclass
class Point:
    x: float
    y: float
    
    def distance_to_origin(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5

# 普通类需要大量样板代码
class PointOld:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __repr__(self):
        return f"Point(x={self.x}, y={self.y})"
    
    def __eq__(self, other):
        if not isinstance(other, PointOld):
            return False
        return self.x == other.x and self.y == other.y
```

> [!TIP] 何时用 dataclass
> - 数据容器（类似 Java 的 POJO）
> - 需要 `__repr__`、`__eq__` 等自动生成
> - 不需要复杂业务逻辑

##### 7.8.6 一图总结

```
┌─────────────────────────────────────────────────────────────┐
│                        类 (Class)                           │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  类属性 (shared)        Dog.species = "犬科"          │  │
│  ├───────────────────────────────────────────────────────┤  │
│  │  类方法 (@classmethod)                                 │  │
│  │    def from_dog(cls, name): return cls(name)         │  │
│  ├───────────────────────────────────────────────────────┤  │
│  │  静态方法 (@staticmethod)                              │  │
│  │    def is_valid_name(name): return bool(name)        │  │
│  ├───────────────────────────────────────────────────────┤  │
│  │  实例方法 (instance)      dog.bark()                   │  │
│  │    def bark(self): return f"{self.name}叫！"          │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ 实例化
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      对象 (Object)                          │
│  dog = Dog("旺财", 3)                                       │
│  - dog.name, dog.age 是实例属性                              │
│  - dog.species 可以访问类属性                                │
│  - dog.bark() 调用实例方法                                  │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                      函数 (Function)                        │
│  def foo(x): return x * 2                                   │
│  - 不属于任何类                                              │
│  - 模块级别定义                                              │
│  - 可以作为参数传递、赋值给变量                               │
└─────────────────────────────────────────────────────────────┘
```

##### 7.8.7 Python 一切皆对象

```python
# 这个概念在 Python 中是真实的

# 1. 类是对象
print(type(Dog))  # <class 'type'>

# 2. 函数是对象
def foo(): pass
print(type(foo))  # <class 'function'>

# 3. 类实例是对象
dog = Dog("旺财", 3)
print(type(dog))  # <class '__main__.Dog'>

# 4. 字符串是对象
s = "hello"
print(type(s))  # <class 'str'>

# 5. 甚至类本身也是 type 的实例
print(isinstance(Dog, type))  # True
```

> [!TIP] 一等公民的具体表现
> 在 Python 中，函数、类、甚至类型都是对象，可以：
> - 赋值给变量：`f = foo`
> - 作为参数传递：`map(f, items)`
> - 作为返回值：`return foo`
> - 存储在数据结构中：`[foo, bar]`

---

### 8. 输入输出

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
