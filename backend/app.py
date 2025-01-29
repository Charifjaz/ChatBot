from flask import Flask, request, jsonify
from flask_cors import CORS  # Add this
from transformers import AutoTokenizer, AutoModelForCausalLM

app = Flask(__name__)
CORS(app)  # Enable CORS

# Model loading with error handling
try:
    model_name = "EleutherAI/pythia-70m"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    tokenizer.pad_token = tokenizer.eos_token  # Set pad token
except Exception as e:
    print(f"Error loading model: {e}")
    exit(1)

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        if not data or "message" not in data:
            return jsonify({"error": "Invalid request"}), 400
            
        user_input = data["message"][:500]  # Basic input sanitization
        
        inputs = tokenizer(user_input, return_tensors="pt")
        
        outputs = model.generate(
            inputs.input_ids,
            max_new_tokens=50,
            temperature=0.7,  # Add creativity control
            top_p=0.9,        # Add diversity control
            pad_token_id=tokenizer.eos_token_id
        )
        
        # Extract only the generated text (excluding input)
        response = tokenizer.decode(
            outputs[0][inputs.input_ids.shape[-1]:], 
            skip_special_tokens=True
        )
        
        return jsonify({"response": response.strip()})
    
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)