import sys
from naturerec_web import create_app

environment = sys.argv[1] if len(sys.argv) > 1 else "development"
create_app(environment).run()
