# This is use to run scheduled run in Jenkins
from common.database import Database
import  app

Database.initialize()
app.check_price_selenium()









