"""Semantic Network"""

class Concept:
	def __init__(self, slug, transitive=1, inverse=None):
		self.slug = slug
		self.m_objects = {}
		self.m_subjects = {}

		# a relation @ is transitive if
		# A @ B and B @ C implies A @ C
		self.transitive = transitive

		if inverse:
			self.inverse = inverse
			inverse.inverse = self
		else:
			self.inverse = None

	def __str__(self):
		return self.slug
	
	def __repr__(self):
		return str(self)

	def objects(self, predicate):
		try: ans = self.m_objects[predicate]
		except: ans = []
		if predicate.transitive:
			# if it's a transitive predicate,
			# pursue recursively
			for i in tuple(ans):
				ans = ans + i.objects(predicate)
		return ans

	def subjects(self, predicate):
		try: ans = self.m_subjects[predicate]
		except: ans = []
		if predicate.inverse and predicate.inverse.transitive:
			# if its inverse is a transitive predicate,
			# pursue recursively
			for i in tuple(ans):
				ans = ans + i.subjects(predicate)
		return ans

	def store_object(self,predicate,object):
		try:
			lst = self.m_objects[predicate]
			if object not in lst: lst.append(object)
		except:
			self.m_objects[predicate] = [object]

	def store_subject(self, predicate, subject):
		try:
			lst = self.m_subjects[predicate]
			if subject not in lst: lst.append(subject)
		except:
			self.m_subjects[predicate] = [subject]

	# Get all the objects of a particular relation,
	# where this (self) is the subject.  These are cumulative.
	# Note that there is no way currently for a subclass to
	# override a base class; it can only extend it.
	def get_objects(self, predicate):
		out = self.objects(predicate)
		# also check type-ancestors (base classes)
		try: parents = self.m_objects[IS_A]
		except: return out
		for p in parents:
			out = out + p.get_objects(predicate)
		return out

	# Get all the subjects of a particular predicate,
	# where this (self) is the object.  These are cumulative.
	def get_subjects(self, predicate):
		out = self.subjects(predicate)
		# also check type-ancestors (base classes)
		try: parents = self.m_objects[IS_A]
		except: return out
		for p in parents:
			out = out + p.get_subjects(predicate)
		return out

	def __call__(self, subject, object=None):
		# when used as a function, check to see whether
		# this predicate applies
		obs = subject.get_objects(self)
		if not object: return obs
		if not obs or object not in obs: return 0
		else: return 1


Predicate = Concept


class Fact:
	def __init__(self, subject, predicate, object):
		self.subject = subject
		self.predicate = predicate
		self.object = object

		# stuff into dictionaries, for searching
		subject.store_object(predicate, object)
		object.store_subject(predicate, subject)

		# deduce inverse relations as well
		if predicate.inverse:
			object.store_object(predicate.inverse, subject)
			subject.store_subject(predicate.inverse, object)


# declare global "is-a" relationship.
# other modules MUST properly use this, rather than
# define their own "is-a", since it has special meaning (inheritance).

IS_A = Predicate("is-a", 1)
EXAMPLE_OF = Predicate("exampleOf", 1, IS_A)

# functions to allow outside access to these objects more easily:
def get_is_a(): return IS_A
def get_example_of(): return EXAMPLE_OF
