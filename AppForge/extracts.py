
from typing import Optional

def extract_error(log: str, ignore_path_str: Optional[str] = None,):
    """
    Extract compilation errors from build log output.
    
    Args:
        log (str): The complete build log output as a string.
        ignore_path_str (Optional[str]): Path string to remove from error messages
            for cleaner output. If None, paths are preserved.
            
    Returns:
        Optional[str]: Extracted error messages as a single string, or None if
            no errors were found. Returns empty string if errors were detected
            but no specific error messages were captured.
    """
    build_outputs = log.split('\n')
    errors = []
    for id,s in enumerate(build_outputs):
        if s.find('编译失败')>=0:
            for kid in range(id,len(build_outputs)):
                if build_outputs[kid].find('BUILD FAILED')>=0:
                    if ignore_path_str:
                        errors = [i.replace(ignore_path_str,'')for i in build_outputs[id+1:kid+1]]
                    else:
                        errors = [i for i in build_outputs[id+1:kid+1]]
                    break
            if(len(errors)==0):
                errors += ['']
    if (len(errors)==0):
        return None
    return '\n'.join(errors)
    
    
def extract_fuzz(log: str):
    """
    Extract fuzzing results from fuzzing log output.
    
    This function analyzes the fuzzing log to detect various types of crashes
    and failures that occurred during the fuzzing process, including native crashes,
    Java crashes, ANRs (Application Not Responding), and startup failures.
    
    Args:
        log (str): The complete fuzzing log output as a string.
        
    Returns:
        dict: A dictionary containing fuzzing results with the following keys:
            - no_crash (int): 1 if no crashes detected in any cycle, 0 otherwise
            - native (int): 1 if native crash detected, 0 otherwise
            - java (int): 1 if Java crash detected, 0 otherwise
            - anr (int): 1 if ANR detected, 0 otherwise
            - failtostart (int): 1 if app failed to start, 0 otherwise   
    """
    result = {
        'compile':0,
        'no_crash':0,
        'native':0,
        'java':0,
        'anr':0,
        'failtostart':0,
    }
    if 'Starting app...' in log:
        result['compile'] = 1
    cycles = log.split('Starting app...')
    crash_cnt,cycle_cnt = 0,0
    for i in cycles[1:]:
        cycle_cnt += 1
        if 'Native crash detected!' in i:
            crash_cnt += 1
            result['native'] = 1
        if 'Java crash detected!' in i:
            crash_cnt += 1
            result['java'] = 1
        if 'ANR detected!' in i:
            crash_cnt += 1
            result['anr'] = 1
        if 'Failed to start' in i:
            crash_cnt += 1
            result['failtostart'] = 1
    if cycle_cnt:
        if crash_cnt==0:
            result['no_crash'] = 1
        
    return result
    
def extract_test(log: str):
    """
    Extract test execution results from test log output.
    
    This function parses the test log to determine compilation success and
    calculate test pass rate based on success/failure counts in the log.
    
    Args:
        log (str): The complete test log output as a string.
        
    Returns:
        dict: A dictionary containing test results with the following keys:
            - compile (int): 1 if compilation was successful (tests executed),
                            0 if no tests were executed
            - test (float): Test pass rate as a float between 0.0 and 1.0,
                            representing the ratio of passed tests
            - all_pass (int): 1 if all tests passed, 0 otherwise
            
    """
    result = {
        'compile':0,
        'test':0.0,
        'all_pass':0
    }
    
    bad, good = log.count("'success': False"), \
                        log.count("'success': True")
    if good+bad > 0:
        result['compile'] = 1
        result['test'] = good / (good+bad)
        if bad == 0:
            result['all_pass'] = 1

    return result