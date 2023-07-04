import logging, time
import kaldi_active_grammar

logging.basicConfig(level=20)
model_dir = "C:/Users/user/Documents/kaldi_model_daanzu_20211030-biglm/kaldi_model"  # Default
tmp_dir = None  # Default

kaldi_active_grammar.disable_donation_message()


##### Set up grammar compiler & decoder

compiler = kaldi_active_grammar.Compiler(model_dir=model_dir, tmp_dir=tmp_dir)
# compiler.fst_cache.invalidate()
decoder = compiler.init_decoder()

##### Set up a rule




rule = kaldi_active_grammar.KaldiRule(compiler, 'Only piece')
fst = rule.fst

# Construct grammar in a FST
initial_state = fst.add_state(initial=True)

state_one = fst.add_state()
fst.add_arc(initial_state, state_one, "move")

state_two = fst.add_state()
for word in ['king', 'queen', 'rook', 'bishop', 'knight', 'pawn']: fst.add_arc(state_one, state_two, word)



from_location_state = fst.add_state()
fst.add_arc(state_two, from_location_state, "at")

from_location_letter_state = fst.add_state()
for word in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']: fst.add_arc(from_location_state, from_location_letter_state, word)

from_location_number_state = fst.add_state()
for word in ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight']: fst.add_arc(from_location_letter_state, from_location_number_state, word)




state_three = fst.add_state()
fst.add_arc(state_two, state_three, "to")
fst.add_arc(from_location_number_state, state_three, "to")


state_four = fst.add_state()
for word in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']: fst.add_arc(state_three, state_four, word)

state_five = fst.add_state()
for word in ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight']: fst.add_arc(state_four, state_five, word)


# Akzeptierender Endzustand
final_state = fst.add_state(final=True)
fst.add_arc(state_five, final_state, None)  # Übergang zum Endzustand



rule.compile()
rule.load()







##### You could add many more rules...

##### Perform decoding on live, real-time audio from microphone

from audio import VADAudio
audio = VADAudio()
audio_iterator = audio.vad_collector(nowait=True)
print("Listening...")

in_phrase = False
for block in audio_iterator:

    if block is False:
        # No audio block available
        time.sleep(0.001)

    elif block is not None:
        if not in_phrase:
            # Start of phrase
            kaldi_rules_activity = [True]  # A bool for each rule
            in_phrase = True
        else:
            # Ongoing phrase
            kaldi_rules_activity = None  # Irrelevant

        decoder.decode(block, False, kaldi_rules_activity)
        output, info = decoder.get_output()
        print("Partial phrase: %r" % (output,))
        recognized_rule, words, words_are_dictation_mask, in_dictation = compiler.parse_partial_output(output)

    else:
        # End of phrase
        decoder.decode(b'', True)
        output, info = decoder.get_output()
        expected_error_rate = info.get('expected_error_rate', float('nan'))
        confidence = info.get('confidence', float('nan'))

        recognized_rule, words, words_are_dictation_mask = compiler.parse_output(output)
        is_acceptable_recognition = bool(recognized_rule)
        parsed_output = ' '.join(words)
        print("End of phrase: eer=%.2f conf=%.2f%s, rule %s, %r" %
            (expected_error_rate, confidence, (" [BAD]" if not is_acceptable_recognition else ""), recognized_rule, parsed_output))

        in_phrase = False








