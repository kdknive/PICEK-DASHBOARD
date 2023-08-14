from apps import db

class Group(db.Model):
  __table_args__ = {'extend_existing': True}
  groupID = db.Column(db.Integer, primary_key=True)
  groupName = db.Column(db.Text, nullable=True)
  created = db.Column(db.Text, nullable=True)
  parentID = db.Column(db.Integer, nullable=True)

  def __repr__(self):
    return '<groupID {}>'.format(self.groupID)
  
  def serialize(self):
    return {
      'groupID': self.groupID,
      'groupName': self.groupName,
      'created':self.created,
      'parentID':self.parentID
    }