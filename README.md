# 公欲善其事，必先利其器

## 1. Python

### 1.1 安装Python
#### Windows系统

1. 访问Python官网下载页面：https://www.python.org/downloads/
2. 选择Python **3.11**版本的Windows安装包
3. 下载完成后运行安装程序
4. 在安装界面勾选"Add Python 3.11 to PATH"
5. 点击"Install Now"开始安装
6. 安装完成后，打开powershell，输入以下命令验证安装:
```bash
python --version
```

#### MacOS系统

1. 推荐使用Homebrew包管理器安装：

   ```bash
   # 安装Homebrew（如果尚未安装）
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   
   # 使用Homebrew安装Python 3
   brew install python@3.11
   ```

3. 安装完成后，验证安装：
   ```bash
   python3 --version
   ```

4. 打开terminal，设置别名使`python`默认指向Python 3：
   ```bash
   # 根据你使用的shell，选择对应的配置文件
   # 如果使用bash
   echo 'alias python=python3' >> ~/.bashrc
   source ~/.bashrc
   
   # 如果使用zsh
   echo 'alias python=python3' >> ~/.zshrc 
   source ~/.zshrc
   ```

### 1.2 安装pip
如果你是按照上面的方法安装，你应该已经安装了pip。可以在命令行验证安装：
```bash
pip --version
```

### 1.3 Poetry
我推荐大家使用Poetry来管理Python的虚拟环境。

#### Windows系统安装Poetry
1. 打开PowerShell并运行：
```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
```

2. 将Poetry添加到系统环境变量，添加以下路径：
```
%APPDATA%\Python\Scripts
```

3. 重启PowerShell，验证安装：
```powershell
poetry --version
```

#### MacOS系统安装Poetry
1. 打开终端，运行以下命令：
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

2. 将Poetry添加到PATH（根据使用的shell选择）：
```bash
# 如果使用bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# 如果使用zsh
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

3. 验证安装：
```bash
poetry --version
```

#### Poetry基本用法
安装完成后，建议进行以下配置：

```bash
# 增加一个package到项目中
poetry add pandas

# 删除一个package
poetry remove pandas

# 查看项目中安装的package
poetry show

# 安装项目中所有package
poetry install

# 进入虚拟环境
poetry shell
```


## 2. Cursor
下载Cursor：https://www.cursor.com/

打开左侧的工具栏，找到“扩展/Extensions”，安装以下三个扩展：

- Python:作者 MS-Python
- Python Debugger:作者 MS-Python
- Chinese(Simplified):作者 MS-CEINTL


配置默认自动保存。

- Cursor->首选项(Preferences)->设置(Settings)->文件编辑器(Editor)->文件（Files）->自动保存(Auto Save)。
- 选择onFocusChange


# Labs

## Lab 1

学习在AI辅助编程的前提下，快速上手一个ML项目。可以在本地完成，也可以使用Google Colab。使用Google Colab时，需要解压data/loan_data.zip为csv文件并上传

Ask LLM for help

- Question 1: 如何使得EDA中的scatter plot 不要挤在X轴的左侧
- Question 2: 如何理解结果汇报中数据，什么是F1 score，什么是ROC curve？什么是AUC。F1 score和AUC的区别是什么？


## Lab 2




## Lab 3


## Lab 4


## Lab 5

## Lab 6

## Lab 7
