from flask import Flask, request, render_template, redirect, url_for, session, jsonify
import opening_ninja

# 1. initializing
app = Flask(__name__)
app.secret_key = 'session_cookieee'

# 2. preparing routes
@app.route("/")
def main():
  return render_template('index.html')

@app.route('/store-session', methods=['POST'])
def store_session():
  session['username'] = request.form.get('username_input')
  session['side_choice'] = request.form.get('side_choice')
  return redirect(url_for('analysis_page'))

@app.route('/analysis')
def analysis_page():
  return render_template('analysis.html')

@app.route('/perform-calc-and-analysis')
def calc_and_analysis():
  username = session.get('username')
  side_choice = session.get('side_choice')
  archived_games = opening_ninja.retrieve_chess_data(username=username, archived=True)
  compilation_of_games = opening_ninja.compile_the_games(archived_games, u_n=username)
  analysis_result = list(opening_ninja.analysis_for_sideColors(compilation_of_games, username=username))

  if side_choice == 'White':
    preserve_ordered_data = list(analysis_result[0].items())
    return jsonify(ar={'White': preserve_ordered_data})
  if side_choice == 'Black':
    preserve_ordered_data = list(analysis_result[1].items())
    return jsonify(ar={'Black': preserve_ordered_data})
  else:
    return jsonify(ar={'White': list(analysis_result[0].items()),
                       'Black': list(analysis_result[1].items())})

# 1. initializing
if __name__ == '__main__':
  app.run()