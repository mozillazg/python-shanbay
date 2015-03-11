
.. module:: shanbay.api


.. autoclass:: API
   :members:

   .. automethod:: user(url='https://api.shanbay.com/account/')
   .. automethod:: word(word, url='https://api.shanbay.com/bdc/search/')
   .. automethod:: add_word(word_id, url='https://api.shanbay.com/bdc/learning/')
   .. automethod:: examples(word_id, type=None, url='https://api.shanbay.com/bdc/example/')
   .. automethod:: add_example(word_id, original, translation, url='https://api.shanbay.com/bdc/example/')
   .. automethod:: favorite_example(example_id, url='https://api.shanbay.com/bdc/learning_example/')
   .. automethod:: delete_example(example_id, url='https://api.shanbay.com/bdc/example/{example_id}/')
   .. automethod:: notes(word_id, url='https://api.shanbay.com/bdc/note/')
   .. automethod:: add_note(self, word_id, note, url='https://api.shanbay.com/bdc/note/')
   .. automethod:: favorite_note(note_id, url='https://api.shanbay.com/bdc/learning_note/')
   .. automethod:: delete_note(note_id, url='https://api.shanbay.com/bdc/note/{note_id}/')

