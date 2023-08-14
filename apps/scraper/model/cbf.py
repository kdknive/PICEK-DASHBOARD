from apps import db

class CBF(db.Model):
  __table_args__ = {'extend_existing': True}
  cbfID = db.Column(db.Integer, primary_key=True, autoincrement=True)
  cbfName = db.Column(db.Text, nullable=True)
  biro = db.Column(db.Text, nullable=True)
  platform = db.Column(db.Text, nullable=True)
  repo = db.Column(db.Boolean, nullable=True)
  pipeline = db.Column(db.Boolean, nullable=True)
  generate = db.Column(db.Boolean, nullable=True)
  approval = db.Column(db.Boolean, nullable=True)
  deploy = db.Column(db.Boolean, nullable=True)
  restart = db.Column(db.Boolean, nullable=True)
  keterangan = db.Column(db.Text, nullable=True)
  possibleMatch = db.Column(db.Text, nullable=True)
  

  def __repr__(self):
    return '<cbfID {}>'.format(self.cbfID)
  
  def serialize(self):
    return {
      'cbfID': self.cbfID,
      'cbfName': self.cbfName,
      'biro':self.biro,
      'platform':self.platform,
      'repo':self.repo,
      'pipeline':self.pipeline,
      'generate':self.generate,
      'approval':self.approval,
      'deploy':self.deploy,
      'restart':self.restart,
      'keterangan':self.keterangan,
      'possibleMatch':self.possibleMatch,
    }