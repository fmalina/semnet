from semnet import *

# get the global "is-a" relationship
isa = get_is_a()

# inverse of "is-a" is "exampleOf"
example = get_example_of()

# declare some concepts we want to store knowledge about
thing = Concept("thing")
animal = Concept("animal")
bird = Concept("bird")
fish = Concept("fish")
minnow = Concept("minnow")
trout = Concept("trout")
ape = Concept("ape")

# declare some facts: what's what?
Fact(animal, isa, thing)
Fact(ape, isa, animal)
Fact(bird, isa, animal)
Fact(fish, isa, animal)
Fact(trout, isa, fish)
Fact(minnow, isa, fish)

# print out some of the things we know (directly or by induction)
print("trout is:", trout.objects(isa))
print("animal is:", animal.objects(isa))
print()
print("fish:", fish.objects(example))
print("fish:", fish.subjects(isa))
print("animals:", animal.subjects(isa))
print()

# declare size relationships
biggerThan = Predicate("bigger than", 1)
smallerThan = Predicate("smaller than", 1, biggerThan)

# declare a couple facts
Fact(minnow, smallerThan, trout)
Fact(trout, smallerThan, ape)

# look at all the things we know now!
print("ape is a fish?", isa(ape, fish))
print("minnow is a fish?", isa(minnow, fish))
print("minnow is an animal?", isa(minnow, animal))
print()
print("ape bigger than minnow?", biggerThan(ape, minnow))
print("minnow bigger than trout?", biggerThan(minnow, trout))
print("minnow is smaller than:", minnow.objects(smallerThan))
print("ape is bigger than:", ape.objects(biggerThan))

# declare concepts for actions
act = Concept("act")
swim = Concept("swim")
walk = Concept("walk")
Fact(swim, isa, act)
Fact(walk, isa, act)

# declare an "ableTo" relation, so we can say who can do what
ableTo = Predicate("ableTo", 0)
whatCan = Predicate("whatCan", 0, ableTo)

# note that fish can swim and apes can walk
Fact(fish, ableTo, swim)
Fact(walk, whatCan, ape)

# see what we can say about swimming ability
print()
print("fish can swim?", ableTo(fish, swim))
print("minnow can swim?", ableTo(minnow, swim))
print("bird can swim?", ableTo(bird, swim))
print("what can swim?", swim.get_objects(whatCan))
print("what can act?", act.get_objects(whatCan))

# declare a "has" relationship (and its inverse)
has = Predicate("has", 0)
whatHas = Predicate("whatHas", 0, has)

scales = Concept("scales")
hair = Concept("hair")
Fact(fish, has, scales)
Fact(ape, has, hair)

print()
print("minnow has hair?", has(minnow, hair))
print("minnow has scales?", has(minnow, scales))
print("ape has hair?", has(ape, hair))
print("ape has scales?", has(ape, scales))
print("what has scales?", scales.get_subjects(has))
