class Customer():
  def __init__(self, id, name, address, email = "", password = ""):
    self.id = id
    self.name = name
    self.address = address
    self.email = email
    self.password = password
    
  def serialized(self):
    """Modifies the output of a Customer instance"""
    return {"name": self.name, "address": self.address, "email": self.email}
