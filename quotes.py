import random

MEANS = {
	'eye_area': 2.0,
	'eye_length': 12.038686,
	'nose_width': 2.557662,
	'nose_length': 8.9533901,
	'brightness': 107.6363
}

STANDARD_DEVIATIONS = {
	'eye_area': 2.0,
	'eye_length': 3.0807754,
	'nose_width': 1.83055801,
	'nose_length': 2.9145182,
	'brightness': 19.127324
}

INSULTS = {
	'big_eyes': [
		'Are your eyes footballs or golf balls?',
		'Are you a person or an anime character?'
	],
	'small_eyes': [
		'Your eyes look like coin slots.',
		"Are you sure you're opening your eyes?",
		'Its okay, you can open them, the Basilisk is dead'
	],
	'big_eye_distance': [
		'Your eyes are so far apart you can fit another face between them.',
		'Something something chameleon.',
		'How does it feel like to have predatory vision?',
		'Did your last pair of glasses break whilst stretching to reach both your eyes?'
	],
	'small_eye_distance': [
		"If your eyes were any closer you'd be a cyclop",
		'How does the world look like in 2D? Do you even have depth perception?'
	],
	'wide_nose': [
		'Is that a gas mask on your face? ',
		'Your nose is so big it makes bloodhounds jealous',
		'Is it a bird, a plane, or your nose?',
		'With a nose like that, you could catch a crosswind and sail away'
	],
	'narrow_nose': [
		'If I smelt that bad my nose would shrink too',
		"Haven't you heard what they say about small noses? It's all proportional..."
	],
	'long_nose': [
		'Is that a gas mask on your face? ',
		'Your nose is so big it makes bloodhounds jealous',
		'Is it a bird, a plane, or your nose?',
		'With a nose like that, you could catch a crosswind and sail away',
		'Your nose is so long it stretches from LA to NYC'
	],
	'short_nose': [
		'If I smelt that bad my nose would shrink too',
		"Haven't you heard what they say about small noses? It's all proportional..."
	],
	'hair': [
		'Your hair makes you look as dumb as a Harvard student',
		'Your hair makes you look as dumb as a Yale student',
		'Your hair makes you look as dumb as a Princeton student',
		'Your hair makes you look as dumb as a Caltech student'
	],
	'lips_sealed': [
		"If my teeth were that yellow I'd keep my lips sealed too",
		"Thanks for keeping your mouth shut, we won't have to hear your worthless opinion"
	],
	'lips_open': [
		'I know I make your jaw drop, but close your mouth, we can smell you from behind the screen',
		'The chinese say if you open your mouth too much all your intelligence leaks out'
	],
	'mood': [
		"Of course you're _____. We can read you like a book",
		'Its okay to be _____. This app is pretty intense'
	],
	'glasses': [
		'What are you looking at, 4 eyes?'
	],
	'male': [
		'Another male-hackathon goer. Why am I not surprised'
	],
	'female': [
		'A girl? At MIT? Right',
	],
	'smiling': [
		"I won't smile that much if I were you, we can all see your teeth",
		'I wish I could be like you. Happy and blissfully unaware of the world around me. '
	],
	'not_smiling': [
		"You can smile. It's okay, I won't bite.",
		"Its good you're not smiling. We don't need terrifying apparitions of the Joker."
	],
	'dark_background': [
		"Of course you're in a dark dungeon you pervert",
		"It's good that the lights are dim. That way no one can see you."
	],
	'light_background': [
		'The sun nice, but melanoma is not',
		"What's the point of the nice bright background? Your Instagram filter will screw it up anyway, you little hipster"
	]
}

def negative(data):
	choices = [
		get_insult_z_score('big_eyes', 'eye_area', 1, data),
		get_insult_z_score('small_eyes', 'eye_area', 0, data),
		get_insult_z_score('big_eye_distance', 'eye_length', 1, data),
		get_insult_z_score('small_eye_distance', 'eye_length', 0, data),
		get_insult_z_score('wide_nose', 'nose_width', 1, data),
		get_insult_z_score('narrow_nose', 'nose_width', 0, data),
		get_insult_z_score('long_nose', 'nose_length', 1, data),
		get_insult_z_score('short_nose', 'nose_length', 0, data),
		get_insult_z_score('dark_background', 'brightness', 0, data),
		get_insult_z_score('light_background', 'brightness', 1, data)
	]

	# random from 0 to 2
	# if gender 'male' then male else female
	choices.append([0.5, random_insult('male') if data['gender']=='male' else random_insult('female')])

	# random from 0 to 2
	# any from hair
	choices.append([0.5, random_insult("hair")])

	# random from 0 to 2
	# any from mood
	# replace _____ with mood
	choices.append([0.2, random_insult("mood").replace("_____", data['mood'])])

	# random from 0 to 2
	# if glasses
	# glasses
	if data['glasses'] == 'true':
		choices.append([1, random_insult("glasses")])

	# random from 0 to 2
	# if smiling 'true' then smiling else not_smiling
	choices.append([0.2, random_insult('smiling') if data['smiling']=='true' else random_insult('not_smiling')])

	choices = filter(lambda x: x != None, choices)

	return choices

def random_choice(choices):
	# Based on http://stackoverflow.com/questions/3679694/a-weighted-version-of-random-choice
	total = sum(w for w, c in choices)
	r = random.uniform(0, total)
	upto = 0
	for w, c in choices:
		if upto + w > r:
			return c
		upto += w
	assert False, "Shouldn't get here"

def random_insult(key):
	return random.choice(INSULTS[key])

def get_insult_z_score(insult_key, data_key, order, data):
	mu = MEANS[data_key]
	sigma = STANDARD_DEVIATIONS[data_key]
	x = data[data_key]
	z_score = (x - mu)/sigma

	if x == 0.0: return None
	
	if (order == 1 and z_score > 0) or (order == 0 and z_score < 0):
		z_score = abs(z_score)
		return [z_score, random_insult(insult_key)]
	else:
		return None

def positive(data):
	return [1,"You must have serious self-doubt issues if you're scared of a computer insulting you"]

