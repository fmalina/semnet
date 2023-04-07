from semnet import *

isa = get_is_a()
example = get_example_of()

g_predicates = {'isa': isa, 'exampleOf': example}
g_concepts = {}


def ask_yes_no(prompt, default='Y'):
	while 1:
		ans = input(f'{prompt} [{default}] ')
		if len(ans) > 1: ans = ans[0]
		if ans == '': ans = default
		if ans == 'y' or ans == 'Y': return 1
		if ans == 'n' or ans == 'N': return 0
		print("Please enter Y or N.")


def handle_command(cmd, concepts=g_concepts, predicates=g_predicates):
	"""Respond to a command from the user"""
	words = cmd.lower().split()
	if words[0] in ('concept', 'c', 'entity', 'e'):
		concepts[words[1]] = Concept(words[1])
	elif words[0] in ('predicate', 'p', 'relation', 'r'):
		trans = ask_yes_no("Transitive?")
		opp = input("Opposite? ").lower()
		predicates[words[1]] = Predicate(words[1],trans)
		if opp:
			predicates[opp] = Predicate(opp,trans, \
				predicates[words[1]])
	elif words[0] == 'list':
		print("Concepts:", concepts.keys())
		print("Predicates:", predicates.keys())
	else:
		subject = concepts[words[0]]
		predicate = predicates[words[1]]
		if words[2][-1] == '?':
			object = concepts[words[2][:-1]]
			handle_question(subject, predicate, object)
		else:
			object = concepts[words[2]]
			handle_statement(subject, predicate, object)

def handle_question(subject, predicate, object):
	if predicate(subject,object): print("yes")
	else: print("no")

def handle_statement(subject, predicate, object):
	if predicate(subject, object):
		print("I already knew that.")
	else:
		Fact(subject, predicate, object)
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

