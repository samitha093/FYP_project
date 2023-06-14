receivedModels = []
def create_model(id, value, accuracy):
    return {
        "id": id,
        "value": value,
        "accuracy": accuracy
    }

def create_received_models(id, value, accuracy):
    global receivedModels 
    model = create_model(id, value, accuracy)
    receivedModels.append(model)
    return receivedModels

def create_data(iteration,localModel,received_models,aggregatedModel):
    data = {
        "iteration": iteration,
        "localModel": localModel,
        "receivedModel": receivedModels,
        "aggregatedModel": aggregatedModel
    }
    return data

localModel = create_model("0001", True, 0.58)

received_models = create_received_models("0002", True, 0.58)
received_models = create_received_models("0003", True, 0.58)
received_models = create_received_models("0004", True, 0.58)

aggregatedModel = create_model("0005", True, 0.92)

# print(localModel)
# print(received_models)
# print(aggregatedModel)
iteration =1
data = create_data(iteration,localModel,received_models,aggregatedModel)

print(data)

# data = {
#     "iteration": 1,
#     "localModel": {"id": "0001", "value": True, "accuracy": 0.58},
#     "receivedModel": [
#         {"id": "0001", "value": True, "accuracy": 0.88},
#         {"id": "0002", "value": True, "accuracy": 0.88},
#         {"id": "0003", "value": True, "accuracy": 0.88},
#         {"id": "0004", "value": True, "accuracy": 0.88}
#     ],
#     "aggregatedModel": {"id": "0005", "value": True, "accuracy": 0.92}
# }

# # Accessing and printing values
# print("Iteration:", data["iteration"])
# print("Local Model ID:", data["localModel"]["id"])
# print("Local Model Value:", data["localModel"]["value"])
# print("Local Model Accuracy:", data["localModel"]["accuracy"])
# print()

# print("Received Models:")
# for i, model in enumerate(data["receivedModel"], start=1):
#     print(f"Received Model {i} ID:", model["id"])
#     print(f"Received Model {i} Value:", model["value"])
#     print(f"Received Model {i} Accuracy:", model["accuracy"])
#     print()

# print("Aggregated Model Value:", data["aggregatedModel"]["value"])
# print("Aggregated Model Accuracy:", data["aggregatedModel"]["accuracy"])
