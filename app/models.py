from datetime import datetime
from . import db

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.now())
    tags = db.Column(db.String(200), nullable=True)

    def __repr__(self):
        return f"<BlogPost {self.title}>"
    
    def set_tags(self, tags_list):
        self.tags = ",".join(tags_list)
    
    def get_tags(self):
        return self.tags.split(",") if self.tags else []
