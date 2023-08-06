from scolar.models import User
def maintest():
	try:
		User.objects.create_superuser('estinadm', 'admin@estin.dz', 'estinadm')
	except:
		pass
