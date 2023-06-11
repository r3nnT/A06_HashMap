# Name: Tyler Renn
# OSU Email: rennt@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: A06 - HashMap
# Due Date: June 11, 2023 @ 11:59 PM
# Description: Implement the HashMap class by completing the provided
# skeleton code in the file hash_map_sc.py.
# Your implementation will include the following methods.


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number and the find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        This method updates the key/value pair in the hash map.
        If the given key already exists in the hash map,
        its associated value must be replaced with the new value.
        If the given key is not in the hash map, a new key/value pair must be added.

        """

        # Resize the table if the load factor exceeds the threshold
        if self.table_load() >= 1.0:
            self.resize_table(
                self._capacity * 2)

        # Compute the hash key for the given key
        h_key = self._hash_function(key) % self._capacity

        # Get the bucket at the computed hash key
        bucket = self._buckets.get_at_index(h_key)

        # If the bucket is empty, insert the key-value pair and update the size
        if bucket.length() == 0:
            bucket.insert(key, value)
            self._size += 1
        else:
            # Iterate through the entry's in the bucket
            for entry in bucket:

                # If the key already exists, update its value
                if entry.key == key:
                    bucket.remove(key)
                    bucket.insert(key, value)
                    return

            # If the key doesn't exist, insert it and update the size
            bucket.insert(key, value)
            self._size += 1

    def empty_buckets(self) -> int:
        """
        This method returns the number of empty buckets in the hash table.
        """
        count = 0
        index = 0
        while index < self._capacity:
            if self._buckets.get_at_index(index).length() == 0:
                count += 1
            index += 1
        return count

    def table_load(self) -> float:
        """
        This method returns the current hash table load factor.
        """
        return self._size / self._capacity

    def clear(self) -> None:
        """
        This method clears the contents of the hash map.
        It does not change the underlying hash
        table capacity.

        """
        self._buckets = DynamicArray()
        self._size = 0

        index = 0
        while index < self._capacity:
            self._buckets.append(LinkedList())
            index += 1

    def resize_table(self, new_capacity: int) -> None:
        """
        This method changes the capacity of the internal hash table.
        All existing key/value pairs must remain in the new hash map,
        and all hash table links must be rehashed.
        (Consider calling another HashMap method for this part).
        """
        if new_capacity < 1:
            return

        # A check for a new capacity with a prime number size
        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)

        # First, create a new HashMap with the new capacity
        new_hash = HashMap(new_capacity, self._hash_function)

        if new_capacity == 2:
            new_hash._capacity = 2

        index = 0
        while index < self._capacity:
            if self._buckets.get_at_index(index).length() > 0:
                for entry in self._buckets.get_at_index(index):
                    new_hash.put(entry.key, entry.value)
            index += 1

        # Reassigning the new values
        self._buckets = new_hash._buckets
        self._size = new_hash._size
        self._capacity = new_hash._capacity

    def get(self, key: str):
        """
        This method returns the value associated with the given key.
        If the key is not in the hash
        map, the method returns None.
        """

        # Compute the hash key for the given key
        h_key = self._hash_function(key) % self._capacity

        # Get the chain (bucket) at the computed hash key
        chain = self._buckets.get_at_index(h_key)

        # If the chain is empty, the key does not exist in the hash map
        if chain.length() == 0:
            return
        else:
            for entry in self._buckets.get_at_index(h_key):

                # If the key matches, return the associated value
                if entry.key == key:
                    return entry.value

        return

    def contains_key(self, key: str) -> bool:
        """
        This method returns True if the given key is in the hash map,
        otherwise it returns False. An
        empty hash map does not contain any keys.
        """

        # Initialize index to traverse the hash map buckets
        index = 0

        # Iterate through each bucket in the hash map
        while index < self._capacity:
            if self._buckets.get_at_index(index).length() > 0:
                for entry in self._buckets.get_at_index(index):

                    # If the key matches, it exists in the hash map
                    if entry.key == key:
                        return True
            index += 1

        return False

    def remove(self, key: str) -> None:
        """
        This method removes the given key and its associated value from the hash map.
        If the key is not in the hash map,
        the method does nothing (no exception needs to be raised).
        """
        index = 0

        # Iterate through each bucket in the hash map
        while index < self._capacity:
            if self._buckets.get_at_index(index).length() > 0:
                for entry in self._buckets.get_at_index(index):

                    # If the key matches, remove the entry
                    if entry.key == key:
                        self._buckets.get_at_index(index).remove(key)
                        self._size -= 1
                        return
            index += 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        This method returns a dynamic array where each index contains
        a tuple of a key/value pair
        stored in the hash map.
        The order of the keys in the dynamic array does not matter.
        """
        new_arr = DynamicArray()
        index = 0

        while index < self._capacity:
            if self._buckets.get_at_index(index).length() > 0:
                for entry in self._buckets.get_at_index(index):

                    # Append the key/value pair to the dynamic array
                    new_arr.append((entry.key, entry.value))
            index += 1

        # Return the dynamic array containing the key/value pairs
        return new_arr


def find_mode(da: DynamicArray) -> (DynamicArray, int):
    """
    Write a standalone function outside of the HashMap class that receives a
    dynamic array (that is not guaranteed to be sorted)
    """

    # Create a new HashMap to store the frequency of values
    map = HashMap()
    i = 0
    newArr_length = da.length()

    while i < newArr_length:
        key = da.get_at_index(i)

        # If the key is not in the map, add it with a count of 1
        if not map.contains_key(key):
            map.put(key, 1)

        # If the key already exists, increment its count
        else:
            map.put(key, map.get(key) + 1)
        i += 1

    occurrence = 0

    # Get the keys and values from the map
    arr = map.get_keys_and_values()
    arr_length = arr.length()

    # Dynamic array to store the most frequent values
    mode_arr = DynamicArray()
    i = 0

    while i < arr_length:

        # If a higher frequency is found, update the frequency variable
        if occurrence < arr.get_at_index(i)[1]:
            occurrence = arr.get_at_index(i)[1]
        i += 1

    i = 0

    while i < arr_length:

        # If the frequency matches the highest frequency,
        # add the key to the mode_arr
        if arr.get_at_index(i)[1] == occurrence:
            mode_arr.append(arr.get_at_index(i)[0])
        i += 1

    # A tuple containing a dynamic array of the
    # most frequent values and the frequency
    return mode_arr, occurrence


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(23, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(53, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
    print(m.get_keys_and_values())

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
