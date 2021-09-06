from django.db import models

# class Post(models.Model):
# 	post_id = models.IntegerField(primary_key=True)
# 	title = models.CharField(max_length=200)
# 	post_content = models.TextField()
# 	post_vote = models.IntegerField(default = 0)

# 	def __str__(self):
# 		return self.title

# class Comment(models.Model):
# 	post_name = models.ForeignKey(Post, on_delete = models.CASCADE)
# 	comment_text = models.TextField()
# 	comment_vote = models.IntegerField(default=0)


# 	def __str__(self):
# 		return self.comment_text
