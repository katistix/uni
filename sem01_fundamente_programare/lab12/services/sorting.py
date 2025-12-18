from typing import List, Callable, TypeVar, Optional, Any

T = TypeVar('T')

def insertion_sort(data: List[T], 
                  key: Optional[Callable[[T], Any]] = None,
                  reverse: bool = False,
                  cmp: Optional[Callable[[T, T], int]] = None) -> List[T]:
    """
    sortare prin inserare cu parametrii optionali
    """
    if not data:
        return data.copy()
    
    # facem o copie pentru a nu modifica originalul
    result = data.copy()
    
    # aplicam functia key daca exista
    if key is not None:
        # cream perechi (key_value, original_element)
        keyed_items = [(key(item), item) for item in result]
        
        # insertion sort pentru perechi (key, value)
        for i in range(1, len(keyed_items)):
            key_item = keyed_items[i]
            j = i - 1
            
            while j >= 0:
                if cmp is not None:
                    # folosesc cmp pe valorile originale
                    comparison = cmp(keyed_items[j][1], key_item[1])
                    should_move = comparison > 0 if not reverse else comparison < 0
                else:
                    # compar cheile
                    should_move = keyed_items[j][0] > key_item[0] if not reverse else keyed_items[j][0] < key_item[0]
                
                if should_move:
                    keyed_items[j + 1] = keyed_items[j]
                    j -= 1
                else:
                    break
            
            keyed_items[j + 1] = key_item
        
        # extragem elementele originale
        result = [item for _, item in keyed_items]
    else:
        # insertion sort direct pe elemente
        for i in range(1, len(result)):
            key_element = result[i]
            j = i - 1
            
            # mut elementele mai mari decat key cu o pozitie la dreapta
            while j >= 0:
                if cmp is not None:
                    comparison = cmp(result[j], key_element)
                    should_move = comparison > 0 if not reverse else comparison < 0
                else:
                    def compare_elements(a: T, b: T) -> bool:
                        try:
                            return a > b  # type: ignore
                        except:
                            return False
                    
                    should_move = compare_elements(result[j], key_element) if not reverse else compare_elements(key_element, result[j])
                
                if should_move:
                    result[j + 1] = result[j]
                    j -= 1
                else:
                    break
            
            # inserez key la pozitia corecta
            result[j + 1] = key_element
    
    return result


def comb_sort(data: List[T], 
             key: Optional[Callable[[T], Any]] = None,
             reverse: bool = False,
             cmp: Optional[Callable[[T, T], int]] = None) -> List[T]:
    """
    sortare comb cu parametrii optionali
    """
    if not data:
        return data.copy()
    
    # facem o copie pentru a nu modifica originalul
    result = data.copy()
    
    # aplicam functia key daca exista
    if key is not None:
        # cream perechi (key_value, original_element)
        keyed_items = [(key(item), item) for item in result]
        
        # comb sort pentru perechi (key, value)
        n = len(keyed_items)
        gap = n
        shrink_factor = 1.3
        sorted_flag = False
        
        while not sorted_flag:
            gap = int(gap / shrink_factor)
            
            if gap <= 1:
                gap = 1
                sorted_flag = True
            elif gap == 9 or gap == 10:
                gap = 11
            
            i = 0
            while i + gap < n:
                should_swap = False
                
                if cmp is not None:
                    # folosesc cmp pe valorile originale
                    comparison = cmp(keyed_items[i][1], keyed_items[i + gap][1])
                    should_swap = comparison > 0 if not reverse else comparison < 0
                else:
                    # compar cheile
                    should_swap = keyed_items[i][0] > keyed_items[i + gap][0] if not reverse else keyed_items[i][0] < keyed_items[i + gap][0]
                
                if should_swap:
                    keyed_items[i], keyed_items[i + gap] = keyed_items[i + gap], keyed_items[i]
                    sorted_flag = False
                
                i += 1
        
        # extragem elementele originale
        result = [item for _, item in keyed_items]
    else:
        # comb sort direct pe elemente
        n = len(result)
        gap = n  # gap initial egal cu lungimea listei
        shrink_factor = 1.3  # factorul de micsorare
        sorted_flag = False
        
        while not sorted_flag:
            # calculez noul gap
            gap = int(gap / shrink_factor)
            
            if gap <= 1:
                gap = 1
                sorted_flag = True  # daca nu sunt schimbari, e sortat
            elif gap == 9 or gap == 10:
                gap = 11  # regula de 11 pentru eficienta
            
            # fac o trecere prin lista cu gap-ul curent
            i = 0
            while i + gap < n:
                should_swap = False
                
                if cmp is not None:
                    comparison = cmp(result[i], result[i + gap])
                    should_swap = comparison > 0 if not reverse else comparison < 0
                else:
                    def compare_elements(a: T, b: T) -> bool:
                        try:
                            return a > b  # type: ignore
                        except:
                            return False
                    
                    should_swap = compare_elements(result[i], result[i + gap]) if not reverse else compare_elements(result[i + gap], result[i])
                
                if should_swap:
                    # schimb elementele
                    result[i], result[i + gap] = result[i + gap], result[i]
                    sorted_flag = False  # a fost o schimbare, nu e sortat
                
                i += 1
    
    return result