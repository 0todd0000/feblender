
from math import sqrt
import numpy as np



class _Tensor(object):
	def __init__(self, x):
		self.x  = x
	def _get_effective(self):
		x0,x1,x2 = self.x[:3]
		a,b,c    = self.x[3:]
		s        = (x0-x1)**2 + (x0-x2)**2 + (x1-x2)**2 + 6*(a*a + b*b + c*c)
		return sqrt(0.5*s)
	def get_x(self):
		return self.x[0]
	def get_y(self):
		return self.x[1]
	def get_z(self):
		return self.x[2]
	def get_xy(self):
		return self.x[3]
	def get_xz(self):
		return self.x[5]
	def get_yz(self):
		return self.x[4]
	def get_principal_1(self):
		return self.get_principal()[0]
	def get_principal_2(self):
		return self.get_principal()[1]
	def get_principal_3(self):
		return self.get_principal()[2]
	def get_principal(self):
		A      = self.tomatrix()
		x      = np.linalg.eigvals(A)
		s0,s2  = x.max(), x.min()
		s1     = x.sum() - s0 - s2
		return np.array([s0,s1,s2])
	def tomatrix(self):
		A      = np.diag(self.x[:3])
		A[0,1] = A[1,0] = self.x[3]
		A[0,2] = A[2,0] = self.x[5]
		A[1,2] = A[2,1] = self.x[4]
		return np.matrix(A)


class _TensorField(object):
	def __init__(self, Y):
		self.Y           = np.asarray(Y, dtype=float)
		self.nElements   = Y.shape[0]
		self.nComponents = Y.shape[1]
		self._check_shape()
		
	def _check_shape(self):
		if self.nComponents != 6:
			raise(  UserError('Tensor fields must be (N x 6) arrays, where N is the number of elements.')  )
			
	def get_effective(self):
		return np.array([_Tensor(y)._get_effective()   for y in self.Y])



class StrainTensor(_Tensor):
	def get_effective_strain(self):
		return self._get_effective()


class StressTensor(_Tensor):
	def get_principal_dev(self):
		A      = self.tomatrix_dev()
		return np.linalg.eigvals(A)
	def get_max_shear(self):
		x      = self.get_principal()
		return 0.5*(x[0]-x[2])
	def get_von_mises(self):
		return self._get_effective()
	def get_effective_stress(self):
		return self._get_effective()
	def tomatrix_dev(self):
		A  = self.tomatrix()
		return A - np.trace(A)/3.0*np.eye(3)


class StrainTensorField(_TensorField):
	pass
class StressTensorField(_TensorField):
	pass




def _tensorfield2effective(Y):
	field   = _TensorField(Y)
	return field.get_effective()
	
def strain_tensor_field_to_effective_strain_field(Y):
	return _tensorfield2effective(Y)
def stress_tensor_field_to_vonmises_stress_field(Y):
	return _tensorfield2effective(Y)




