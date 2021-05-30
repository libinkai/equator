# 配置

## 账号配置

```
$ git config --global user.name "Your Name"
$ git config --global user.email "email@example.com"
```

## 自定义Git

- 让Git显示颜色，会让命令输出看起来更醒目`$ git config --global color.ui true`

## 配置命令别名

- `$ git config --global alias.st status`

## 配置文件

- 每个仓库的Git配置文件都放在`.git/config`文件中
- 当前用户的Git配置文件放在用户主目录下的一个隐藏文件`.gitconfig`中

# 版本管理

> 版本控制系统只能跟踪文本文件的改动，比如TXT文件，网页，所有的程序代码等等；图片、视频、Word文档这些二进制文件，虽然也能由版本控制系统管理，但没法跟踪文件的变化，只能把二进制文件每次改动串起来

## 初始化仓库并追踪文件

```shell
# 初始化
$ git init
# 添加追踪文件
$ git add readme.txt
# 提交
$ git commit -m "wrote a readme file"
# 查看当前仓库状态
$ git status
# 查看具体修改的内容（工作区和版本库里面最新版本的区别）
$ git diff readme.txt
# 查看提交历史
$ git log [--pretty=oneline]
# 版本回退（HEAD表示当前版本，HEAD^表示前一个版本，HEAD~n表示前n个版本）
$ git reset --hard HEAD^
# 查看每一次提交的ID（前进版本时适用）
$ git reflog
```

## 分区

- 工作区（Working Directory）：在电脑里能看到的目录
- 版本库（Repository）：隐藏目录`.git`。
- Git的版本库里存了很多东西，其中最重要的就是称为stage（或者叫index）的暂存区，还有Git为我们自动创建的第一个分支`master`，以及指向`master`的一个指针叫`HEAD`
- `git add`把文件添加进去，实际上就是把文件修改添加到暂存区，`git commit`提交更改，实际上就是把暂存区的所有内容提交到当前分支
- Git跟踪的是文件的修改而不是文件本身，每次修改，如果不用`git add`到暂存区，那就不会加入到`commit`中

## 撤销修改

### 撤销工作区修改

- `$ git checkout -- readme.txt`把`readme.txt`文件在工作区的修改全部撤销，这里有两种情况：
  - 一种是`readme.txt`自修改后还没有被放到暂存区，现在，撤销修改就回到和版本库一模一样的状态；
  - 一种是`readme.txt`已经添加到暂存区后，又作了修改，现在，撤销修改就回到添加到暂存区后的状态。

总之，就是让这个文件回到最近一次`git commit`或`git add`时的状态。

### 撤销暂存区的修改

- `git reset HEAD `可以把暂存区的修改撤销掉（unstage），重新放回工作区
- `git reset`命令既可以回退版本，也可以把暂存区的修改回退到工作区

### 撤销版本库的修改

- 已经提交了不合适的修改到版本库时，想要撤销本次提交，需要版本回退（前提是没有推送到远程库）

## 远程仓库

### 添加远程仓库

- 添加远程仓库`$ git remote add origin git@github.com:michaelliao/learngit.git`

- 推送本地仓库到远程仓库`git push -u origin master`。第一次推送`master`分支时，加上了`-u`参数，Git不但会把本地的`master`分支内容推送的远程新的`master`分支，还会把本地的`master`分支和远程的`master`分支关联起来，在以后的推送或者拉取时就可以简化命令，只需要`$ git push origin master`

### 克隆远程仓库

- 假设我们从零开发，那么最好的方式是先创建远程库，然后，从远程库克隆

- 克隆`$ git clone git@github.com:michaelliao/gitskills.git`

### 管理

- 查看远程库信息，使用`git remote -v`

### 推送

- 推送全部分支，`git push --all`

# 分支管理

## 创建分支

```
$ git checkout -b dev
# git checkout命令加上-b参数表示创建并切换，相当于以下两条命令
$ git branch dev
$ git checkout dev
Switched to branch 'dev'
```

## 合并分支

```shell
$ git checkout master
$ git merge dev
git merge命令用于合并指定分支到当前分支
```

- `Fast-forward`合并是“快进模式”，也就是直接把`master`指向`dev`的当前提交，所以合并速度非常快

## 删除分支

```
$ git branch -d dev
```

## 查看分支

```
$ git branch
```

## 切换分支

> 切换分支使用`git checkout `，而前面讲过的撤销修改则是`git checkout -- `，同一个命令，有两种作用，不推荐使用check out切换分支

- 创建并切换到新的`dev`分支，`$ git switch -c dev`

- 直接切换到已有的`master`分支，`$ git switch master`

## 冲突解决

- Git用`<<<<<<<`，`=======`，`>>>>>>>`标记出不同分支的内容
- 当Git无法自动合并分支时，就必须首先解决冲突。解决冲突后，再提交，合并完成。解决冲突就是把Git合并失败的文件手动编辑为我们希望的内容，再提交。
- 用`git log --graph`命令可以看到分支合并图

## 分支管理策略

- 合并分支时，如果可能，Git会用`Fast forward`模式，但这种模式下，删除分支后，会丢掉分支信息
- 如果要强制禁用`Fast forward`模式，Git就会在merge时生成一个新的commit，这样，从分支历史上就可以看出分支信息
- `$ git merge --no-ff -m "merge with no-ff" dev`，因为本次合并要创建一个新的commit，所以加上`-m`参数，把commit描述写进去

- `master`分支应该是非常稳定的，也就是仅用来发布新版本，平时不能在上面干活；干活都在`dev`分支上，也就是说，`dev`分支是不稳定的；团队的每个人都在`dev`分支上干活，每个人都有自己的分支，时不时地往`dev`分支上合并就可以了

  ![avatar](W:\leaning\note\归纳总结\git\协作分支策略.png)

## BUG分支

- `$ git stash`可以把当前工作现场“储藏”起来，等以后恢复现场后继续工作

- `$ git stash list`查看隐藏的工作区内容

- 恢复内容，一是用`git stash apply`恢复，但是恢复后，stash内容并不删除，你需要用`git stash drop`来删除；

  另一种方式是用`git stash pop`，恢复的同时把stash内容也删了

- `$ git cherry-pick 4c805e2`命令，让我们能复制一个特定的提交到当前分支。（当在BUG分支上fix一个BUG时，可以把这个过程复制到当前分支）

- 开发一个新feature，最好新建一个分支；如果要丢弃一个没有被合并过的分支，可以通过`git branch -D `强行删除

## 多人协作

- 多人协作的工作模式通常是这样：
  1. 首先，可以试图用`git push origin `推送自己的修改；
  2. 如果推送失败，则因为远程分支比你的本地更新，需要先用`git pull`试图合并；
  3. 如果合并有冲突，则解决冲突，并在本地提交；
  4. 没有冲突或者解决掉冲突后，再用`git push origin `推送就能成功！
- 如果`git pull`提示`no tracking information`，则说明本地分支和远程分支的链接关系没有创建，用命令`git branch --set-upstream-to <branch-name> origin/<branch-name>`

## 变基 ReBase？

- rebase操作可以把本地未push的分叉提交历史整理成直线。rebase的目的是使得我们在查看历史提交的变化时更容易，因为分叉的提交需要三方对比。

# 标签管理

- 发布一个版本时，我们通常先在版本库中打一个标签（tag），这样，就唯一确定了打标签时刻的版本。将来无论什么时候，取某个标签的版本，就是把那个打标签的时刻的历史版本取出来。所以，标签也是版本库的一个快照。（tag就是一个让人容易记住的有意义的名字，它跟某个commit绑在一起）

## 创建

- 切换到需要打标签的分支上，然后`$ git tag v1.0`
- 默认标签是打在最新提交的commit上的，对某次commit打标签`$ git tag v0.9 f52c633`

- 用命令`git tag`查看标签
- 用`git show `查看标签信息
- 还可以创建带有说明的标签，用`-a`指定标签名，`-m`指定说明文字`$ git tag -a v0.1 -m "version 0.1 released" 1094adb`

## 删除

- `$ git tag -d v0.1`，创建的标签都只存储在本地，不会自动推送到远程。所以，打错的标签可以在本地安全删除。
- 如果要推送某个标签到远程，使用命令`git push origin `
- 推送全部`$ git push origin --tags`

- 命令`git push origin :refs/tags/`可以删除一个远程标签

  