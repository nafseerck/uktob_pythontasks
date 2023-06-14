from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/sum', methods=['POST'])
def calculate_sum():
    try:
        data = request.get_json()
        numbers = data['numbers']
        if not isinstance(numbers, list):
            raise ValueError('Invalid input. "numbers" must be a list.')
        total = sum(numbers)
        return jsonify({'sum': total})
    except KeyError:
        return jsonify({'error': 'Invalid input. "numbers" key not found.'}), 400
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@app.route('/concatenate', methods=['POST'])
def concatenate_strings():
    try:
        data = request.get_json()
        string1 = data['string1']
        string2 = data['string2']
        if not isinstance(string1, str) or not isinstance(string2, str):
            raise ValueError('Invalid input. Both "string1" and "string2" must be strings.')
        result = string1 + string2
        return jsonify({'concatenated_string': result})
    except KeyError:
        return jsonify({'error': 'Invalid input. Required keys not found.'}), 400
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run()
