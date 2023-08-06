from scolar.models import User
def maintest():
	User.objects.create_superuser('estinadm', 'admin@estin.dz', 'estinadm')
