from apps import db

class Project(db.Model):
  projectID = db.Column(db.Integer, primary_key=True)    
  project = db.Column(db.Text, nullable=True)
  created = db.Column(db.Text, nullable=True)
  updated = db.Column(db.Text, nullable=True)
  path = db.Column(db.Text, nullable=True)
  exist = db.Column(db.Boolean, nullable=True)
  environment = db.Column(db.Text, nullable=True)
  url = db.Column(db.Text, nullable=True)
  new = db.Column(db.Boolean, nullable=True)
  parentID = db.Column(db.Integer, nullable=True)
  oldestJob = db.Column(db.Text, nullable=True)
  newestJob = db.Column(db.Text, nullable=True)
    
  def __repr__(self):
    return '<projectID {}>'.format(self.projectID)
  
  def serialize(self):
    return {
      'projectID': self.projectID,
      'project':self.project,
      'created':self.created,
      'updated':self.updated,
      'path': self.path,
      'exist':self.exist,
      'environment':self.environment,
      'url':self.url,
      'new':self.new,
      'parentID':self.parentID,
      'oldestJob': self.oldestJob,
      'newestJob': self.newestJob
    }