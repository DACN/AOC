import re
from collections import Counter
from collections import defaultdict 
from aocd.models import Puzzle
import sys
import timeit
import time
from operator import itemgetter


def split_on_empty_lines(s):
    # greedily match 2 or more new-lines
    blank_line_regex = r"(?:\r?\n){2,}"
    return re.split(blank_line_regex, s.strip())


def lines_to_list(s):
    lines = s.split('\n')
    fun_list = []
    for line in lines[1:]:
        fun_list.append(list(int(match.group()) for match in re.finditer(r'\d+', line)))
    return fun_list


def aoc_dict(x, name, lines):
    '''take a value x and maps it using the data in lines'''
    for line in lines:
        if line[1] <= x < line[1]+line[2]:
            return line[0]+x-line[1]
    return x


def aoc_map(x, name, lines):
    '''like aoc_dict but also returns the longest potential span'''
    for line in lines:
        if line[1] <= x < line[1]+line[2]:
            return line[0]+x-line[1],line[1]+line[2]-x
    return x,1

def aoc_range(pair, name, lines):
    '''takes a pair and maps it to multiple pairs using the data in lines'''
    span_left = pair[1]
    first_value = pair[0]
    pairs = []
    while span_left > 0:
        mapped_value, potential_span = aoc_map(first_value, name, lines)
        # print(f"12 {mapped_value=}, {potential_span=}")
        pair = mapped_value, min(span_left, potential_span)
        pairs.append(pair)
        first_value = first_value + min(span_left, potential_span)
        span_left = span_left - potential_span
    return pairs


def aoc_ranges(pairs, name, lines):
    '''takes a pair and maps it to multiple pairs using the data in lines'''
    mapped_pairs = []
    for pair in pairs:
        # print(f"2: aoc_ranges: {pair=}")
        mapped_pairs.extend(aoc_range(pair, name, lines))
    return mapped_pairs

def seed_to_soil_ranges(pairs):
    return aoc_ranges(pairs, 'seed-to-soil',            seed_to_soil_data)
def soil_to_fertilizer_ranges(pairs):     
    return aoc_ranges(pairs, 'soil-to-fertilizer'     , soil_to_fertilizer_data)
def fertilizer_to_water_ranges(pairs):    
    return aoc_ranges(pairs, 'fertilizer-to-water'    , fertilizer_to_water_data)
def water_to_light_ranges(pairs):         
    return aoc_ranges(pairs, 'water-to-light'         , water_to_light_data)
def light_to_temperature_ranges(pairs):   
    return aoc_ranges(pairs, 'light-to-temperature'   , light_to_temperature_data)
def temperature_to_humidity_ranges(pairs):
    return aoc_ranges(pairs, 'temperature-to-humidity', temperature_to_humidity_data)
def humidity_to_location_ranges(pairs):   
    return aoc_ranges(pairs, 'humidity-to-location'   , humidity_to_location_data)

def seed_to_soil(x):
    return aoc_dict(x, 'seed-to-soil',            seed_to_soil_data)
def soil_to_fertilizer(x):     
    return aoc_dict(x, 'soil-to-fertilizer'     , soil_to_fertilizer_data)
def fertilizer_to_water(x):    
    return aoc_dict(x, 'fertilizer-to-water'    , fertilizer_to_water_data)
def water_to_light(x):         
    return aoc_dict(x, 'water-to-light'         , water_to_light_data)
def light_to_temperature(x):   
    return aoc_dict(x, 'light-to-temperature'   , light_to_temperature_data)
def temperature_to_humidity(x):
    return aoc_dict(x, 'temperature-to-humidity', temperature_to_humidity_data)
def humidity_to_location(x):   
    return aoc_dict(x, 'humidity-to-location'   , humidity_to_location_data)


def puzzle1(x):
    locs = []
    seeds = list(int(match.group()) for match in re.finditer(r'\d+', input[0]))
    for s in seeds:
        loc = humidity_to_location(   
                temperature_to_humidity(
                light_to_temperature(   
                water_to_light(      
                fertilizer_to_water(    
                soil_to_fertilizer(     
                seed_to_soil(s)))))))
        locs.append(loc)
    return min(locs)


def puzzle2(x):
    seed_pair_strings = list(match.group() for match in re.finditer(r'\d+\s\d+', input[0]))
    seed_pairs = []    
    for pair in seed_pair_strings:
        seed_pairs.append(list(int(match.group()) for match in re.finditer(r'\d+', pair)))
    mapped_pairs = humidity_to_location_ranges(   
                temperature_to_humidity_ranges(
                light_to_temperature_ranges(   
                water_to_light_ranges(      
                fertilizer_to_water_ranges(    
                soil_to_fertilizer_ranges(     
                seed_to_soil_ranges(seed_pairs)))))))
    mapped_pairs.sort()
    return mapped_pairs[0][0]
    # 15290096



def get_puzzle_data(year, day, test):
    puzzle="""seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4"""
    input = split_on_empty_lines(puzzle)
    if not test:
        puzzle = Puzzle(year=2023, day=5)
        input = split_on_empty_lines(puzzle.input_data)
    return input

def extend_the_lines(lines):
    small = 0
    big = 1000_000_000_000_000_000_000_000_000_000
    extended_lines = []
    lines = sorted(lines, key=itemgetter(1))
    for line in lines:
        if line[1]-small > 0:
            extended_lines.append([small, small, line[1]-small])
        extended_lines.append(line)
        small = line[1] + line[2]
    extended_lines.append([small, small, big])
    return extended_lines


if __name__=="__main__":
    test = False
    start = time.time()
    input = get_puzzle_data(2023, 5, test)
    # print(input)
    assert input[0].startswith('seeds')
    assert input[1].startswith('seed-to-soil')            
    assert input[2].startswith('soil-to-fertilizer')     
    assert input[3].startswith('fertilizer-to-water')    
    assert input[4].startswith('water-to-light')         
    assert input[5].startswith('light-to-temperature')   
    assert input[6].startswith('temperature-to-humidity')
    assert input[7].startswith('humidity-to-location')   


    seed_to_soil_data = lines_to_list(input[1])
    soil_to_fertilizer_data = lines_to_list(input[2])
    fertilizer_to_water_data = lines_to_list(input[3])
    water_to_light_data = lines_to_list(input[4])
    light_to_temperature_data = lines_to_list(input[5])
    temperature_to_humidity_data = lines_to_list(input[6])
    humidity_to_location_data = lines_to_list(input[7])

    seed_to_soil_data =            extend_the_lines(seed_to_soil_data)     
    soil_to_fertilizer_data =      extend_the_lines(soil_to_fertilizer_data)       
    fertilizer_to_water_data =     extend_the_lines(fertilizer_to_water_data)     
    water_to_light_data =          extend_the_lines(water_to_light_data)         
    light_to_temperature_data =    extend_the_lines(light_to_temperature_data)    
    temperature_to_humidity_data = extend_the_lines(temperature_to_humidity_data)   
    humidity_to_location_data =    extend_the_lines(humidity_to_location_data)      


    print(f"{puzzle1(input)=}")
    # 424490994

    print(f"{puzzle2(input)=}")
    # 15290096

    print(time.time()-start)