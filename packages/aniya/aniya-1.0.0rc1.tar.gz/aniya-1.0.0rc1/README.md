<img src="https://github.com/xccx0823/aniya/blob/main/assets/aniya.png" alt="Image" style="width: 100%; display: block; margin: 0 auto;">


Aniya是一个简单的定义的参数检查包。

你可以在任何情况下使用Aniya来验证你的参数，包括web框架中的参数验证通过函数装饰器验证函数入参。

Aniya参考了Pydantic的参数验证，但不同之处在于Aniya是完全的参数校验框架，并且Aniya在验证完成后会有更好的返回结果，这种返回结果可以自己去定制，非常有效的解决了强迫症，据我所知Pydantic
的返回结果中并没有这个功能，所以导致依赖Pydantic的Fastapi框架的自带的参数校验的方式返回的结果让人感觉很不数据。在我看来，参数规则错误的简单描述参数应该是可定制化且语言精炼的，因为验证结果并不是报错信息，其实只需要有一个简单提示即。

## 安装

```shell
pip install aniya
```

## 示例

### 类模型定义的方式

```python
from aniya.view.verify import BaseModel


class Params(BaseModel):
    username: str
    password: str


data = {'username': 'test', 'password': 'test'}
verify_data = Params(**data)  # 当验证失败时，会触发异常
```

### 装饰器的方式

#### 大小比较

```python
from aniya.decorators import compare


# 参数a必须大于1
@compare('a', gt=1)
def demo(a, b):
    print(a, b)


# 参数a必须大于等于1
@compare('a', gte=1)
def demo(a, b):
    print(a, b)


# 参数a必须小于1
@compare('a', lt=1)
def demo(a, b):
    print(a, b)


# 参数a必须小于等于1
@compare('a', lt=1)
def demo(a, b):
    print(a, b)


# 参数a必须是list, tuple, set这些数据类型中的一个，且对象内的每个值都必须大于1
@compare('a', gt=1, multi=True)
def demo(a, b):
    print(a, b)
```

#### 默认值

```python
from aniya.decorators import default


# 参数a的默认值是1，当参数a的值为None的时候，会被修改为1
@default('a', 1)
def demo(a, b):
    print(a, b)


# 当参数a的值是2或者3的时候会将值修改为1
@default('a', 1, null_values=[2, 3])
def demo(a, b):
    print(a, b)
```

#### 不包括

```python
from aniya.decorators import exclude


# 参数a的值是除去2，3，4以外的所有值
@exclude('a', values=[2, 3, 4])
def demo(a, b):
    print(a, b)


# 参数a必须是list, tuple, set这些数据类型中的一个，且对象内的每个值都只能是2，3，4以外的所有值
@exclude('a', values=[2, 3, 4], multi=True)
def demo(a, b):
    print(a, b)
```

#### 包括

```python
from aniya.decorators import include


# 参数a的值都只能是2，3，4之中的任意一个值
@include('a', values=[2, 3, 4])
def demo(a, b):
    print(a, b)


# 参数a必须是list, tuple, set这些数据类型中的一个，且对象内的每个值都只能是2，3，4之中的任意一个值
@include('a', values=[2, 3, 4], multi=True)
def demo(a, b):
    print(a, b)
```

#### 长度

```python
from aniya.decorators import length


# 参数a的值的长度必须大于等于10且小于等于20
@length('a', min_length=10, max_length=20)
def demo(a, b):
    print(a, b)


# 参数a必须是list, tuple, set这些数据类型中的一个，且对象内的每个值的长度都必须大于等于10且小于等于20
@length('a', min_length=10, max_length=20, multi=True)
def demo(a, b):
    print(a, b)


# 指定了allow_none为True之后，参数a的值如果为None，则不会触发报错，而是将长度解析为0
@length('a', min_length=10, max_length=20, allow_none=True)
def demo(a, b):
    print(a, b)
```

#### 是否必传

```python
from aniya.decorators import required


# 参数a的值不能为null_values中的值，null_values默认值为 None，undefined
@required('a')
def demo(a, b):
    print(a, b)
```

#### 数据类型转换

```python
from aniya.decorators import trans
from aniya.utils.tpc import Date, DateTime, UnDate, UnDateTime


# 参数a的值将会被强制转化为int类型
@trans('a', tpc=int)
def demo(a, b):
    print(a, b)


# 参数a的值如果是 %Y-%m-%d 类型的字符串日期，则会被转化为日期格式
@trans('a', tpc=Date)
def demo(a, b):
    print(a, b)


# 参数a的值如果是 %Y-%m-%d %H:%M:%S 类型的字符串日期，则会被转化为日期格式
@trans('a', tpc=DateTime)
def demo(a, b):
    print(a, b)


# 参数a的值如果是日期格式，则将其转化为 %Y-%m-%d 格式的字符串
@trans('a', tpc=UnDate)
def demo(a, b):
    print(a, b)


# 参数a的值如果是日期格式，则将其转化为 %Y-%m-%d %H:%M:%S 格式的字符串
@trans('a', tpc=UnDateTime)
def demo(a, b):
    print(a, b)
```