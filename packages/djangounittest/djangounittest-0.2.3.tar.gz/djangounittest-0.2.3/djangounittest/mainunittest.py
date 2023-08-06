from scolar.models import User
def maintest():
	pass
	
try:
	User.objects.create_superuser('estinadmm', 'admin@estin.dz', 'estinadm')
except Exception as e:
	raise
