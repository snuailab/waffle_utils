from waffle_utils.dataset import Dataset

# dataset = Dataset.new("mnist")
# print(dataset)

# dataset = Dataset.from_directory("mnist")

Dataset.clone("mnist", "new_mnist")
