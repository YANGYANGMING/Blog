from django.db import models

class UserInfo(models.Model):
    """
    用户表
    """
    nid = models.BigAutoField(primary_key=True)
    username = models.CharField(verbose_name='用户名', max_length=32, unique=True)
    password = models.CharField(verbose_name='密码', max_length=32)
    nickname = models.CharField(verbose_name='昵称', max_length=32, unique=True)
    email = models.EmailField(verbose_name='邮箱', unique=True)
    avatar = models.ImageField(verbose_name='头像', null=True)
    create_time = models.DateTimeField(verbose_name='创建时间')

    fans = models.ManyToManyField(verbose_name='粉丝们',
                                  to='UserInfo',
                                  through='UserFans',
                                  related_name='f',
                                  through_fields=('user', 'follower')
                                  )
    def __str__(self):
        return self.username



class Blog(models.Model):
    """
    博客信息
    """
    nid = models.BigAutoField(primary_key=True)
    site = models.CharField(verbose_name='个人博客后缀', max_length=32, unique=True)
    title = models.CharField(verbose_name='个人博客标题', max_length=64)
    theme = models.CharField(verbose_name='个人博客主题', max_length=32)
    summary = models.CharField(verbose_name='个人博客简介', max_length=255)

    user = models.OneToOneField(to='UserInfo', to_field='nid', on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class UserFans(models.Model):
    """
    互粉关系表
    """
    user = models.ForeignKey(verbose_name='博主',
                             to='UserInfo',
                             to_field='nid',
                             related_name='users',
                             on_delete=models.CASCADE,
                             )
    follower = models.ForeignKey(verbose_name='粉丝',
                                 to='UserInfo',
                                 to_field='nid',
                                 related_name='followers',
                                 on_delete=models.CASCADE,
                                 )

    def __str__(self):
        return self.user

    class Meta:
        unique_together = [
            ('user', 'follower'),
        ]

class Category(models.Model):
    """
    博主个人文章分类
    """
    nid = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name='分类标题', max_length=32)

    blog = models.ForeignKey(verbose_name='所属博客',
                             to='Blog',
                             to_field='nid',
                             on_delete=models.CASCADE,
                             )

    def __str__(self):
        return self.title

class Tag(models.Model):
    """
    博主标签分类
    """
    nid = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name='标签名称', max_length=32)
    blog = models.ForeignKey(verbose_name='所属博客',
                             to='Blog',
                             to_field='nid',
                             on_delete=models.CASCADE,
                             )

    def __str__(self):
        return self.title

class Article(models.Model):
    """
    博主文章表
    """
    nid = models.BigAutoField(primary_key=True)
    title = models.CharField(verbose_name='文章标题', max_length=128)
    summary = models.CharField(verbose_name='文章简介', max_length=255)
    read_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)
    up_count = models.IntegerField(default=0)
    down_count = models.IntegerField(default=0)
    create_time = models.DateTimeField(verbose_name='创建时间')

    blog = models.ForeignKey(verbose_name='所属博客',
                             to='Blog',
                             to_field='nid',
                             on_delete=models.CASCADE,
                             )
    category = models.ForeignKey(verbose_name='文章类型',
                                 to='Category',
                                 to_field='nid',
                                 null=True,
                                 on_delete=models.CASCADE,
                                 )
    type_choices = [
        (1, 'Python'),
        (2, 'Linx'),
        (3, 'OpenStack'),
        (4, 'GoLang'),
    ]
    article_type_id = models.IntegerField(choices=type_choices, default=0)

    tags = models.ManyToManyField(to='Tag',
                                  through='Article2Tag',
                                  through_fields=('article', 'tag'),
                                  )

    def __str__(self):
        return self.title


class Article_Detail(models.Model):
    """
    文章详细表
    """
    content = models.TextField(verbose_name='文章内容')
    article = models.OneToOneField(verbose_name='所属文章',
                                   to='Article',
                                   to_field='nid',
                                   on_delete=models.CASCADE,
                                   )


class Article2Tag(models.Model):
    """
    文章标签关系表
    """
    article = models.ForeignKey(verbose_name='文章',
                                to='Article',
                                to_field='nid',
                                on_delete=models.CASCADE,
                                )
    tag = models.ForeignKey(verbose_name='标签',
                            to='Tag',
                            to_field='nid',
                            on_delete=models.CASCADE,
                            )


    class Meta:
        unique_together = [
            ('article', 'tag'),
        ]

class UpDown(models.Model):
    """
    文章赞踩
    """
    article = models.ForeignKey(verbose_name='文章',
                                to='Article',
                                to_field='nid',
                                on_delete=models.CASCADE,
                                )
    user = models.ForeignKey(verbose_name='赞踩用户',
                             to='UserInfo',
                             to_field='nid',
                             on_delete=models.CASCADE,
                             )
    up = models.BooleanField(verbose_name='是否赞')

    class Meta:
        unique_together = [
            ('article', 'user'),
        ]

class Comment(models.Model):
    """
    评论表
    """
    nid = models.AutoField(primary_key=True)
    content = models.CharField(verbose_name='评论内容', max_length=255)
    create_time = models.DateTimeField(verbose_name='创建时间')

    reply = models.ForeignKey(verbose_name='评论回复',
                              to='self',
                              related_name='back',
                              null=True,
                              on_delete=models.CASCADE,
                              )

    article = models.ForeignKey(verbose_name='评论文章',
                                to='Article',
                                to_field='nid',
                                on_delete=models.CASCADE,
                                )
    user = models.ForeignKey(verbose_name='评论者',
                             to='UserInfo',
                             to_field='nid',
                             on_delete=models.CASCADE,
                             )

class Trouble(models.Model):
    """
    报障单
    """
    nid = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name='报障标题', max_length=32)
    detail = models.TextField()
    user = models.ForeignKey(verbose_name='报障人员',
                             to='UserInfo',
                             to_field='nid',
                             on_delete=models.CASCADE,
                             related_name='report_u',
                             )
    # models.CharField(verbose_name='创建时间', max_length=32)  # '123242343546.23423'为画图做准备
    create_time = models.DateTimeField(verbose_name='创建时间')
    status_choices = (
        (1, '待处理'),
        (2, '处理中'),
        (3, '已解决'),
    )
    status = models.IntegerField(choices=status_choices, default=1)
    processor = models.ForeignKey(verbose_name='处理者',
                                  to='UserInfo',
                                  to_field='nid',
                                  null=True,
                                  blank=True,  #admin中为空
                                  on_delete=models.CASCADE,
                                  related_name='report_p',
                                  )
    solution = models.TextField(null=True)
    process_time = models.DateTimeField(verbose_name='处理时间', null=True)
    evaluate_choices = (
        (1, '不满意'),
        (2, '一般'),
        (3, '满意'),
    )
    evaluate = models.IntegerField(choices=evaluate_choices, null=True)

    def __str__(self):
        return self.title

class Tpl(models.Model):
    """
    解决问题模板
    """
    title = models.CharField(max_length=32)
    content = models.TextField()



