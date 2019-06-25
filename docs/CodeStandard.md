# 代码规范

## 前端代码规范

#### vue规范

[参照官网](https://cn.vuejs.org/v2/style-guide/index.html)

------

#### js规范

JavaScript规范使用[ES2016+][1]

代码使用 `ESlint` 作为基本的语法检验工具，规则如下：

- `Eslint Config Standard` 作为基础规则
- 使用分号
- 函数参数列表前需要有括号
- 对象花括号中必须有空格
- 箭头函数参数列表按需添加括号
- 不适用console
- 允许非驼峰式命名
- 基于 `JavaScript Standard Style`][10]`

额外规则：

- 永远不省略分号
- 可以使用Async/Await的地方就不使用Promise
- Vue组建名字采用pascal命名法，即首字母大写的驼峰式命名，如LoginBox.vue
- 组件文件和组件使用相同的名字，组件名必须避免使用Vue保留标签名（包括HTML标签和Vue内部标签）
- JS变量名、参数名、函数名：必须使用camel命名法。

命名同时还需要关注语义，如：

- 变量名应当使用名词camel命名
- boolean类型的应当使用is、has等起头,表示其类型
- 函数名应当用动宾短语

------

#### HTML规范

- HTML标签id、class命名使用camel命名
- HTML标签中的属性必须用双引号包围
- img标签要写alt标签
- 单标签不要写闭合标签（img、link、input、hr、br）
- 自定义属性要以data- 开头
- td要在tr里面，li要在ul/ol里面
- ul/ol的直接子元素只能是li
- section里面要有标题标签
- 使用section标签增强SEO(搜索引擎优化)
- 行内元素里面不可使用块级元素(a标签里面不能放div)
- 要用table布局写邮件模板
- html要保持简洁，不要套太多层
- 特殊情况下才在html里面写script和style
- 样式要写在head标签里
- html要加上lang的属性
- 要在head标签靠前位置写上charset和meta标签
- 特殊符号使用html实体
- img空src的问题
- 关于行内元素空格和换行的影响
- 类的命名使用小写字母加中划线（hello-world)
- 不推荐使用自定义标签
- 重复杂id和重复属性
- 不推荐使用属性设置样式（canvas width height 需要写）
- 使用合适的标签
- 如果内容是表格就使用table，table有自适应的优点；如果是一个列表就使用ol/ul标签，扩展性比较好
- 如果是输入框就使用input，而不是写一个p标签，然后设置contenteditable=true，因为这个在IOS Safari上光标定位容易出现问题。如果需要做特殊效果除外
- 如果是粗体就使用b/strong，而不是自己设置font-weight
- 如果是表单就使用form标签，注意form里面不能套form
- 如果是跳链就使用a标签，而不是自己写onclick跳转。a标签里面不能套a标签
- 使用html5语义化标签，如导航使用nav，侧边栏使用aside，顶部和尾部使用header/footer，页面比较独立的部分可以使用article，如用户的评论。
- 如果是按钮就应该写一个button或者`<input type="button">`，而不是写一个a标签设置样式，因为使用button可以设置disabled，然后使用CSS的:disabled，还有:active等伪类使用，例如在:active的时候设置按钮被按下去的感觉
- 如果是标题就应该使用标题标签h1/h2/h3，而不是自己写一个`<p class="title"></p>`，相反如果内容不是标题就不要使用标题标签了
- 在手机上使用select标签，会有原生的下拉控件，手机上原生select的下拉效果体验往往比较好，不管是IOS还是android，而使用`<input type="tel">`在手机上会弹一个电话号码的键盘，`<input type="number">` `<input type="email">`都会弹相应的键盘
- 如果是分隔线就使用hr标签，而不是自己写一个border-bottom的样式，使用hr容易进行检查
- 如果是换行文本就应该使用p标签，而不是写br，因为p标签可以用margin设置行间距，但是如果是长文本的话使用div，因为p标签里面不能有p标签，特别是当数据是后端给的，可能会带有p标签，所以这时容器不能使用p标签。
- 不要在https的链接里写http的图片

------

#### css规范

------

- 常用控件、表格、布局和页面做出一套或者多套模板。
- `选择器` 与 `{` 之间必须包含空格。
- `属性名` 与之后的 `:` 之间不允许包含空格， `:` 与 `属性值` 之间必须包含空格。
- `列表型属性值` 书写在单行时，`,` 后必须跟一个空格。
- 每行不得超过 `120` 个字符，除非单行不可分割。
- `>`、`+`、`~` 选择器的两边各保留一个空格。
- 属性选择器中的值必须用双引号包围。
- 属性定义必须另起一行。
- 属性定义后必须以分号结尾。
- 选择器的嵌套层级应不大于 3 级，位置靠后的限定条件应尽可能精确。
- 在可以使用缩写的情况下，尽量使用属性缩写。
- 使用 `border` / `margin` / `padding` 等缩写时，应注意隐含值对实际数值的影响，确实需要设置多个方向的值时才使用缩写。
- 同一 rule set 下的属性在书写时，应按功能进行分组，并以 **Formatting Model（布局方式、位置） > Box Model（尺寸） > Typographic（文本相关） > Visual（视觉效果）** 的顺序书写，以提高代码的可读性。
- 当元素需要撑起高度以包含内部的浮动元素时，通过对伪类设置 `clear` 或触发 `BFC` 的方式进行 `clearfix`。尽量不使用增加空标签的方式。
- 尽量不使用 `!important` 声明。
- 文本内容必须用双引号包围。
- 当数值为 0 - 1 之间的小数时，省略整数部分的 `0`。