# encoding=utf-8
# 用户权限常量
# 这里使用八位二进制来保存权限，目前只使用了四位，还有四位空余


class Permission:
    COMMENT = 0x01  # 评论文章
    WRITE_ARTICLES = 0x02  # 写文章
    DEL_COMMENT = 0x04  # 删除评论
    ADMINISTER = 0xff  # 管理员
    DEFAULT = 0x00
