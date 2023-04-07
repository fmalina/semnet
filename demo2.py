from semnet import *

isa = get_is_a()
example = get_example_of()

g_relations = {'isa': isa, 'exampleOf': example}
g_concepts = {}


def ask_yes_no(prompt, default='Y'):
	while 1:
		ans = input(f'{prompt} [{default}] ')
		if len(ans) > 1: ans = ans[0]
		if ans == '': ans = default
		if ans == 'y' or ans == 'Y': return 1
		if ans == 'n' or ans == 'N': return 0
		print("Please enter Y or N.")


def handle_command(cmd, concepts=g_concepts, relations=g_relations):
	"""Respond to a command from the user"""
	words = cmd.lower().split()
	if words[0] in ('concept', 'c', 'entity', 'e'):
		concepts[words[1]] = Concept(words[1])
	elif words[0] in ('relation', 'r'):
		trans = ask_yes_no("Transitive?")
		opp = input("Opposite? ").lower()
		relations[words[1]] = Relation(words[1],trans)
		if opp:
			relations[opp] = Relation(opp,trans, \
				relations[words[1]])
	elif words[0] == 'list':
		print("Concepts:", concepts.keys())
		print("Relations:", relations.keys())
	else:
		subject = concepts[words[0]]
		relation = relations[words[1]]
		if words[2][-1] == '?':
			object = concepts[words[2][:-1]]
			handle_question(subject, relation, object)
		else:
			object = concepts[words[2]]
			handle_statement(subject, relation, object)

def handle_question(subject, relation, object):
	if relation(subject,object): print("yes")
	else: print("no")

def handle_statement(subject, relation, object):
	if relation(subject, object):
		print("I already knew that.")
	else:
		Fact(subject, relation, object)
		print("OK.")


print("Ready. Enter 'quit' (without quotes) to exit.")
cmd = ''
while cmd != 'quit':
	cmd = input("Command? ")
	if cmd != 'quit':
#		try:
			handle_command(cmd)
#		except:
#			print("Error in command.")
#			print("Perhaps you used an undefined term?")

