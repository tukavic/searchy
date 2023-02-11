from transformers import GPT2Tokenizer, GPT2LMHeadModel

# Load the pre-trained GPT-2 model and tokenizer
tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
model = GPT2LMHeadModel.from_pretrained('gpt2')

# Define the text you want to summarize and the prompt
text = "The quick brown fox jumps over the lazy dog. The fox was very fast and agile."
prompt = "Summarize the text: " + text

# Tokenize the prompt
prompt_input_ids = tokenizer.encode(prompt, return_tensors='pt')

# Use the model to generate a summary with the prompt
# text generation example
generated_text_samples = model.generate(
    prompt_input_ids,
    max_length= 50,  
    do_sample=True,  
    top_k=0,
    num_return_sequences= 1
)

# Decode the summary
summary = tokenizer.decode(generated_text_samples[0], skip_special_tokens=True)

# # Print the summary
print(summary)
