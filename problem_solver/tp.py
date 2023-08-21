
payload = [4,8,16,32, 64, 128, 256, 512, 1024]
time = [143.46, 198.25 ,215.24, 245.43, 301.83, 340.24, 392.41, 517.52, 895.18, 468.36 ]

def get_payload_time(target):
    left, right = 0, len(payload) - 1
    closest_index = None
    
    while left <= right:
        mid = (left + right) // 2
        if payload[mid] == target:
            return mid
        elif payload[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
            
        if closest_index is None or abs(payload[mid] - target) < abs(payload[closest_index] - target):
            closest_index = mid
            
    return time[closest_index]