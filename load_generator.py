from flask import Flask, jsonify, request
import requests, time
import threading

def isTreadAlive(threads):
    for t in threads:
        if t.is_alive():
            return 1
    return 0

app = Flask(__name__)
result = []

@app.route('/ping', methods=["GET"])
def ping():
    response = {"success": True}
    return jsonify(response), 200

def request_data(thread_name):
    start = time.time()
    global result
    print(thread_name, " running.")
    try:
        response = requests.get(f"https://cse546p2-309902.wn.r.appspot.com/testScaling").json()
        result.append(response)
        end = time.time()
        print(thread_name ," done:" , len(result), " Total time: ", (end-start))
        return result
    except Exception as e:
        result.append({"status":"Error : "+str(e)})
        end = time.time()
        print(thread_name ," done:" , len(result), " Total time: ", (end-start))
        return result


@app.route('/posts', methods=["GET"])
def posts():
    try:
        start = time.time()
        no_of_threads = 20
        uploadThreads = []
        for i in range(no_of_threads):
            tthread = threading.Thread(
                target=request_data, args=("Thread"+str(i+1),))
            tthread.start()
            uploadThreads.append(tthread)

        while(isTreadAlive(uploadThreads)):
            continue

        end = time.time()
        print( "Total time: ", (end-start))
        return jsonify({"response":result}), 200
    except Exception as e:
        return {"status":"Error :"+str(e)}, 200


if __name__ == '__main__':
    app.run(debug=False)