"""Semantic Network"""

class Concept:
	def __init__(self, slug):
		self.slug = slug
		self.m_objects = {}
		self.m_agents = {}

	def __str__(self):
		return self.slug
	
	def __repr__(self):
		return str(self)

	def objects(self, relation):
		try: ans = self.m_objects[relation]
		except: ans = []
		if relation.transitive:
			# if it's a transitive relation,
			# pursue recursively
			for i in tuple(ans):
				ans = ans + i.objects(relation)
		return ans

	def agents(self, relation):
		try: ans = self.m_agents[relation]
		except: ans = []
		if relation.inverse and relation.inverse.transitive:
			# if its inverse is a transitive relation,
			# pursue recursively
			for i in tuple(ans):
				ans = ans + i.agents(relation)
		return ans

	def store_object(self,relation,object):
		try:
			lst = self.m_objects[relation]
			if object not in lst: lst.append(object)
		except:
			self.m_objects[relation] = [object]

	def store_agent(self, relation, agent):
		try:
			lst = self.m_agents[relation]
			if agent not in lst: lst.append(agent)
		except:
			self.m_agents[relation] = [agent]

	# Get all the objects of a particular relation,
	# where this (self) is the agent.  These are cumulative.
	# Note that there is no way currently for a subclass to
	# override a base class; it can only extend it.
	def get_objects(self, relation):
		out = self.objects(relation)
		# also check type-ancestors (base classes)
		try: parents = self.m_objects[IS_A]
		except: return out
		for p in parents:
			out = out + p.get_objects(relation)
		return out

	# Get all the agents of a particular relation,
	# where this (self) is the object.  These are cumulative.
	def get_agents(self, relation):
		out = self.agents(relation)
		# also check type-ancestors (base classes)
		try: parents = self.m_objects[IS_A]
		except: return out
		for p in parents:
			out = out + p.get_agents(relation)
		return out

class Relation:
	def __init__(self, slug, transitive=1, inverse=None):
		self.slug = slug

		# a relation @ is transitive if
		# A @ B and B @ C implies A @ C
		self.transitive = transitive

		if inverse:
			self.inverse = inverse
			inverse.inverse = self
		else:
			self.inverse = None

	def __str__(self): return self.slug
	def __repr__(self): return str(self)

	def __call__(self, agent, object=None):
		# when used as a function, check to see whether
		# this relation applies
		obs = agent.get_objects(self)
		if not object: return obs
		if not obs or object not in obs: return 0
		else: return 1

class Fact:
	def __init__(self, agent, relation, object):
		self.agent = agent
		self.relation = relation
		self.object = object

		# stuff into dictionaries, for searching
		agent.store_object(relation, object)
		object.store_agent(relation, agent)

		# deduce inverse relations as well
		if relation.inverse:
			object.store_object(relation.inverse, agent)
			agent.store_agent(relation.inverse, object)


# declare global "is-a" relationship.
# other modules MUST properly use this, rather than
# define their own "is-a", since it has special meaning (inheritance).

IS_A = Relation("is-a", 1)
EXAMPLE_OF = Relation("exampleOf", 1, IS_A)

# functions to allow outside access to these objects more easily:
def get_is_a(): return IS_A
def get_example_of(): return EXAMPLE_OF
