# Trong utils.py


def binary_search_range(arr, low, high, target_low, target_high, attribute_index):
    while low <= high:
        mid = (low + high) // 2
        mid_value = arr[mid][attribute_index]

        print(f"Checking mid_value={mid_value} at index={mid}")

        if target_low <= mid_value <= target_high:
            print("Found within the range.")
            return mid
        elif mid_value < target_low:
            print("Moving to the right.")
            low = mid + 1
        else:
            print("Moving to the left.")
            high = mid - 1

    print("Value not found in the specified range.")
    return -1


# Hàm sắp xếp nhanh (quicksort) cho mảng dựa trên một thuộc tính cụ thể.
def quicksort(arr, low, high, attribute_index):
    if low < high:
        # Chia mảng thành các phần nhỏ và lấy chỉ số pivot.
        pi = partition(arr, low, high, attribute_index)

        # Đệ quy sắp xếp các phần nhỏ bên trái và bên phải của pivot.
        quicksort(arr, low, pi - 1, attribute_index)
        quicksort(arr, pi + 1, high, attribute_index)


# Hàm phân hoạch mảng trong quicksort để có thứ tự đúng và trả về chỉ số của pivot.
def partition(arr, low, high, attribute_index):
    i = low - 1
    pivot = arr[high][attribute_index]

    for j in range(low, high):
        if arr[j][attribute_index] <= pivot:
            i = i + 1
            # Hoán đổi vị trí giữa các phần tử để có thứ tự đúng.
            arr[i], arr[j] = arr[j], arr[i]

    # Đưa pivot về đúng vị trí và trả về chỉ số của pivot.
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1