import pprint
from abc import ABC, abstractmethod
from file_handler import FileManager

pp = pprint.PrettyPrinter(indent=2)

ENABLE_BASEPATH = False
class DiffAnalyser(ABC):
    def __init__(self, diff_analyser_type) :
        self.diff_analyser_type = diff_analyser_type

    @abstractmethod
    def find_diff(self):
        pass
    

class OASDiffAnalyser(DiffAnalyser):
    def __init__(self,oas_spec1, oas_spec2):
        super().__init__("OAS")
        self.oas_spec1 = FileManager(oas_spec1).load_json()
        self.oas_spec2 = FileManager(oas_spec2).load_json()
        self.diff = {}
        self.diff["source_file"] = oas_spec1
        self.diff["target_file"] = oas_spec2

    def find_diff(self):
        self.diff[self.diff["source_file"]+"-"+self.diff["target_file"]], self.diff[self.diff["target_file"]+"-"+self.diff["source_file"]] =self.scan_paths()
        return self.diff
        
    def scan_paths(self):
        spec1_scan = {}
        spec2_scan = {}
        if self._get_oas_type(self.oas_spec1)==2:
            spec1_scan = self._scan_paths_oas2(self.oas_spec1)
        elif self._get_oas_type(self.oas_spec1)==3:
            spec1_scan = self._scan_paths_oas3(self.oas_spec1)

        if self._get_oas_type(self.oas_spec2)==2:
            spec2_scan = self._scan_paths_oas2(self.oas_spec2)
        elif self._get_oas_type(self.oas_spec2)==3:
            spec2_scan = self._scan_paths_oas3(self.oas_spec2)

        paths_diff1  = list(set(spec1_scan)-set(spec2_scan)) 
        paths_diff2 = list(set(spec2_scan)- set(spec1_scan))
        return [paths_diff1, paths_diff2]
        
    def _scan_structural_diff(self):
        pass

    def _fetch_allowed_methods_params(self,paths):
        pass

def _get_oas_type(spec):
        oas_ver = 2 if spec.get("swagger", None) else 3 if spec.get("openapi", None) else "Unknown"
        return oas_ver

def _scan_paths_oas2(spec):
        paths = spec.get("paths")
        basepath = spec.get("basePath", "")
        all_paths = paths.keys()
        all_paths_with_basepath = []
        for path in all_paths:
            all_paths_with_basepath.append((basepath + path).replace('//','/'))
        return all_paths_with_basepath, all_paths

        # return basepath, all_paths

def _get_oas3_server(spec):
    server = ""
    server_found= False
    spec_paths = spec.get('paths')
    for path, path_val in spec_paths.items():
        for method, method_val in path_val.items():
            
            if not isinstance(spec_paths.get(path).get(method), dict):
                continue
            if spec_paths.get(path).get(method).get('servers'):
                server = spec_paths.get(path).get(method).get('servers')[0].get('url')
                if server:
                    server_found =True
                    break
        if server_found:
            break
    return server

def _get_oas3_basepath(spec):
    from urllib.parse import urlparse
    server = _get_oas3_server(spec)
    parsed_url = urlparse(server)
    return parsed_url.path




def _scan_paths_oas3( spec):
    paths = spec.get("paths")
    
    all_paths = paths.keys()
    all_paths_with_basepath = []
    basepath = _get_oas3_basepath(spec)
    for path in all_paths:
        all_paths_with_basepath.append((basepath + path).replace('//','/'))
    return all_paths_with_basepath, all_paths


def _generate_aggregated_paths(file_list):
    all_scans = []
    all_scans_without_basepath = []
    for file in file_list:
        oas_spec = FileManager(file).load_json()
        if _get_oas_type(spec = oas_spec)==2:
            spec_scan, spec_scan_without_basepath = _scan_paths_oas2(oas_spec)
        elif _get_oas_type(oas_spec)==3:
            spec_scan, spec_scan_without_basepath = _scan_paths_oas3(oas_spec)
        spec_scan_meta = [[file, path] for path in spec_scan]
        spec_scan_meta_without_basepath = [[file, path] for path in spec_scan_without_basepath]
        all_scans += spec_scan_meta
        all_scans_without_basepath+= spec_scan_meta_without_basepath
    return all_scans, len(all_scans),all_scans_without_basepath

def scan_all_paths(src_files, tar_files):
    paths_src, src_api_count, paths_src_without_basepath = _generate_aggregated_paths(src_files)
    paths_tar, tar_api_count, paths_tar_without_basepath = _generate_aggregated_paths(tar_files)
    paths_src_dict  = {x[1]:x[0] for x in paths_src }
    paths_tar_dict = {x[1]:x[0] for x in paths_tar}
    paths_src_list = [x[1] for x in paths_src]
    paths_tar_list = [x[1] for x in paths_tar]
    paths_src_dict_without_basepath  = {x[1]:x[0] for x in paths_src_without_basepath }
    paths_tar_dict_without_basepath  = {x[1]:x[0] for x in paths_tar_without_basepath }
    paths_src_list_without_basepath = [x[1] for x in paths_src_without_basepath]
    paths_tar_list_without_basepath = [x[1] for x in paths_tar_without_basepath]
    paths_diff1_without_basepath  = list(set(paths_src_list_without_basepath)-set(paths_tar_list_without_basepath)) 
    paths_diff2_without_basepath = list(set(paths_tar_list_without_basepath)- set(paths_src_list_without_basepath))
    paths_common_without_basepath = list(set(paths_src_list_without_basepath).intersection(paths_tar_list_without_basepath))

    paths_diff1  = list(set(paths_src_list)-set(paths_tar_list)) 
    paths_diff2 = list(set(paths_tar_list)- set(paths_src_list))
    paths_common = list(set(paths_src_list).intersection(paths_tar_list))

    paths_diff1_with_file = [[paths_src_dict.get(x), x] for x in paths_diff1]
    paths_diff2_with_file = [[paths_tar_dict.get(x), x] for x in paths_diff2]
    paths_src_dict_transpose = {}
    for path_src in paths_diff1_with_file:
        if path_src[0] in paths_src_dict_transpose:
            paths_src_dict_transpose[path_src[0]].append(path_src[1])
        else:
            paths_src_dict_transpose[path_src[0]] = [path_src[1]]
    paths_tar_dict_transpose = {}
    for path_tar in paths_diff2_with_file:
        if path_tar[0] in paths_tar_dict_transpose:
            paths_tar_dict_transpose[path_tar[0]].append(path_tar[1])
        else:
            paths_tar_dict_transpose[path_tar[0]] = [path_tar[1]]
    return [paths_diff1_with_file, paths_diff2_with_file, \
            src_api_count,tar_api_count, paths_src_dict_transpose,\
            paths_tar_dict_transpose, paths_common, \
            paths_src_dict,paths_tar_dict
            , paths_src_dict_without_basepath,paths_tar_dict_without_basepath,
            paths_common_without_basepath
            ]

def is_hashable(value):
    try:
        hash(value)
        return True
    except TypeError:
        return False
    
def get_methods_metadata_dict(l1):
    # print(l1)
    result_dict = {}
    for x in l1:
        if x[0] not in result_dict:
            result_dict[x[0]] = {}
            result_dict[x[0]]["param_count"] = len(x)-2
            result_dict[x[0]]["data_types"] = {}
            for par_type in x[2:]:
                if not is_hashable(par_type[1]):
                    continue
                if par_type[1] not in result_dict[x[0]]["data_types"]:
                    result_dict[x[0]]["data_types"][par_type[1]] = [1,[par_type[0]]]
                else:
                    result_dict[x[0]]["data_types"][par_type[1]][0] +=1
                    result_dict[x[0]]["data_types"][par_type[1]][1].append(par_type[0])

    return result_dict


def _summary(src_files, tar_files):
    summary = {}
    summary['whats_new'], summary['whats_missing'],\
        summary['count_api_src_files'],summary['count_api_tar_files'],\
            summary['paths_src_dict_transpose'],summary['paths_tar_dict_transpose'],\
                  paths_common, paths_src_dict, paths_tar_dict,\
                      paths_src_dict_without_basepath,paths_tar_dict_without_basepath,\
                         paths_common_without_basepath = scan_all_paths(src_files, tar_files)
    summary['count_src_files'] = len(src_files)
    summary['count_tar_files'] = len(tar_files)
    summary['count_whats_new'] = len(summary['whats_new'])
    summary['count_whats_missing'] = len(summary['whats_missing'])
    diff_paths_methods,src_methods_dict,tar_methods_dict, src_methods_metadata_list,tar_methods_metadata_list = extract_metadata_endpoints(paths_common, paths_src_dict, paths_tar_dict,paths_common_without_basepath,paths_src_dict_without_basepath,paths_tar_dict_without_basepath)
    summary['diff_paths_methods'] = diff_paths_methods
    summary['tar_methods_dict'] = tar_methods_dict
    summary['src_methods_dict'] = src_methods_dict
    summary['src_methods_metadata_list'] = src_methods_metadata_list
    summary['tar_methods_metadata_list'] = tar_methods_metadata_list
    src_methods_metadata_dict = get_methods_metadata_dict(src_methods_metadata_list)
    tar_methods_metadata_dict = get_methods_metadata_dict(tar_methods_metadata_list)
    summary['src_methods_metadata_dict'] = src_methods_metadata_dict
    summary['tar_methods_metadata_dict'] = tar_methods_metadata_dict
    summary['source_system'] = "discovery system"
    summary['target_system'] = "mulesoft system"
    mismatch_param_list = []
    for k,v in src_methods_metadata_dict.items():
        current_list = []
        v2 = tar_methods_metadata_dict.get(k)
        if v.get('param_count') ==0:
            continue
        if v.get('param_count') !=v2.get('param_count'):
            current_list = [k]
            current_list.append(abs(v.get('param_count')-v2.get('param_count')))
        mismatch_param_list.append(current_list)        
    summary['mismatch_param_list'] = mismatch_param_list
    return summary


def resolve_definitions(file,v,  path, method):
    data_types = []
    oas_spec = FileManager(file).load_json()
    if _get_oas_type(oas_spec)==3:
        try:
            if not v:
                requestBody = oas_spec.get('paths').get(path).get(method).get('requestBody')
                if requestBody:
                    requestBody_content = requestBody.get('content')
                    if requestBody_content :
                        v = requestBody_content.get("application/json").get("schema")
        except Exception as e :
            print(e)
    data_types = _resolve_definitions(oas_spec,v, data_types)
    return data_types


def _resolve_definitions(oas_spec,v, data_types):
    try:
        if _get_oas_type(spec = oas_spec)==2:
            def_key = v.get('$ref').split("/")[-1]
            properties = oas_spec.get("definitions").get(def_key).get("properties")
            for property, property_value in properties.items():
                for k,val in property_value.items():
                    if k=="type" and val!="array":
                        data_types.append([property,val])
                        continue
                    elif k=="schema":
                        _resolve_definitions(oas_spec,val, data_types)
                    elif k=="items":
                        _resolve_definitions(oas_spec,val,data_types)
                    elif "$ref" in str(val):
                        _resolve_definitions(oas_spec,val, data_types)
                    elif k == "$ref":
                         _resolve_definitions(oas_spec,{k:val}, data_types)

        elif _get_oas_type(oas_spec)==3:
            if v and v.get('$ref'):
                def_key = v.get('$ref').split("/")[-1]
                properties = oas_spec.get("components").get('schemas').get(def_key).get("properties")
                if not properties:
                    properties = oas_spec.get("components").get('schemas').get(def_key)
                for property, property_value in properties.items():
                    if not isinstance(property_value, dict):
                        if property == "type" and property_value not in ("array","object"):
                            data_types.append([def_key,property_value])
                        elif "$ref" in str(property_value):
                            _resolve_definitions(oas_spec,property_value, data_types)
                        continue

                    for k,val in property_value.items():
                        if k=="type" and val not in ("array","object"):
                            data_types.append([property, val])
                            continue
                        elif k=="schema":
                            _resolve_definitions(oas_spec,val, data_types)
                        elif k=="items":
                            _resolve_definitions(oas_spec,val,data_types)
                        elif "$ref" in str(val):
                            _resolve_definitions(oas_spec,val, data_types)
                        elif k == "$ref":
                            _resolve_definitions(oas_spec,{k:val}, data_types)
                        elif k =="properties":
                            _resolve_definitions(oas_spec,val, data_types)
            else:
            # terminal state
                to_scan =[v]
                while to_scan:
                    curr_val  = to_scan.pop()
                    
                    if isinstance(curr_val, dict):
                        for k1, v1 in curr_val.items():
                            if k1=="type" and v1 not in ('array','object'):
                                data_types.append([curr_val,v1])
                            elif k1=="$ref":
                                _resolve_definitions(oas_spec,{k1:v1}, data_types)
                            else:
                                to_scan.append(v1)
    except Exception as e:
        pass
        # print(e)
        # print(v)
    return data_types
    
def extract_metadata_endpoints(paths, src_file_map, tar_file_map,paths_common_without_basepath,paths_src_dict_without_basepath,paths_tar_dict_without_basepath ):
    diff_paths_methods = []
    src_methods_dict = {}
    tar_methods_dict = {}
    src_methods_metadata_list = []
    tar_methods_metadata_list = []
    for path in paths_common_without_basepath:
        src_file = src_file_map.get(path) 
        tar_file = tar_file_map.get(path)
        if src_file and tar_file:
            if not src_methods_dict.get(src_file):
                src_methods_dict[src_file] = {}
            if not tar_methods_dict.get(tar_file):
                tar_methods_dict[tar_file] = {}
            src_spec, tar_spec = FileManager(src_file).load_json(), FileManager(tar_file).load_json()
            src_path_dict, src_spec_type = _get_path_from_spec(src_spec, path)
            tar_path_dict, tar_spec_type = _get_path_from_spec(tar_spec, path)
            src_methods, src_methods_dict[src_file][path] = _get_method_params_data_list_dicts(src_path_dict, src_spec_type)
            tar_methods, tar_methods_dict[tar_file][path] = _get_method_params_data_list_dicts(tar_path_dict, tar_spec_type)
            diff1 = list(set(src_methods) - set(tar_methods))
            diff2 = list(set(tar_methods) - set(src_methods))
            if diff1:
                diff_paths_methods.append([src_file,tar_file, path, diff1])
            if diff2:
                diff_paths_methods.append([tar_file, src_file, path, diff2])

    for file_path, file_value in src_methods_dict.items():
        oas_spec = FileManager(file_path).load_json()
        for path, path_value in file_value.items():
            for method, method_value in path_value.items():
                temp_list = [path,method]
                for parameter,param_val in method_value.items():
                    for k,v in param_val.items():                  
                        if k=='type' :
                            temp_list.append([parameter, v])
                        elif k== 'schema':
                            data_types = resolve_definitions(file_path,v, path, method)
                            temp_list += data_types
                        if _get_oas_type(oas_spec) == 3:
                            data_types = resolve_definitions(file_path,v, path, method)
                            temp_list += data_types
            src_methods_metadata_list.append(temp_list)

    for file_path, file_value in tar_methods_dict.items():
        oas_spec = FileManager(file_path).load_json()
        for path, path_value in file_value.items():
            for method, method_value in path_value.items():
                temp_list = [path,method]
                if _get_oas_type(oas_spec) == 3:
                    data_types = resolve_definitions(file_path,{}, path, method)
                    temp_list += data_types
                for parameter,param_val in method_value.items():
                    for k,v in param_val.items():
                        if k=='type':
                            temp_list.append([parameter,v])   
                tar_methods_metadata_list.append(temp_list)
    return diff_paths_methods,src_methods_dict, tar_methods_dict, src_methods_metadata_list, tar_methods_metadata_list

def _get_method_params_data_list_dicts(path_dict, spec_type):
    methods_dict = {}
    if spec_type in [2,3]:
        methods = list(path_dict.keys())
    for method,method_value in path_dict.items():
        methods_dict[method] = {}
        if not isinstance(method_value, dict):
            return methods_dict
        parameters = method_value.get('parameters', [])
        if spec_type == 2:
            for parameter in parameters:
                parameter_name = parameter['name']
                in_header = parameter['in']
                required = parameter.get('required', False)
                if parameter.get('type'):
                    parameter_type = parameter['type']
                    methods_dict[method][parameter_name] = {
                        'in': in_header,
                        'required': required,
                        'type': parameter_type
                    }
                elif parameter.get('schema'):
                    parameter_type = parameter.get('schema')
                    methods_dict[method][parameter_name] = {
                        'in': in_header,
                        'required': required,
                        'schema': parameter_type
                    }

        elif spec_type ==3 :
            for parameter in parameters:
                parameter_name = parameter['name']
                in_header = parameter['in']
                required = parameter.get('required', False)
                parameter_type = parameter['schema']['type']

                methods_dict[method][parameter_name] = {
                        'in': in_header,
                        'required': required,
                        'type': parameter_type
                    }
    return methods, methods_dict


def _get_paths_oas2_dict(spec,path):
    paths = spec.get("paths")
    basepath = spec.get("basePath", "")
    all_paths = paths.keys()
    all_paths_with_basepath_dict = {}
    return paths.get((basepath + path).replace('//','/'))
    # for path in all_paths:
    #     all_paths_with_basepath_dict[(basepath + path).replace('//','/')] = paths.get(path)
    # return all_paths_with_basepath_dict, all_paths

def _get_paths_oas3_dict(spec, path):
    paths = spec.get("paths")
    
    all_paths = paths.keys()
    all_paths_with_basepath = []
    basepath = _get_oas3_basepath(spec)
    return paths.get((basepath + path).replace('//','/'))
    # all_paths_with_basepath_dict = {}
    # for path in all_paths:
    #     all_paths_with_basepath_dict[(basepath + path).replace('//','/')] = paths.get(path)
    # return all_paths_with_basepath_dict, all_paths



    return all_paths_with_basepath, all_paths

def _get_path_from_spec(spec, path):
    spec_type = _get_oas_type(spec = spec)
    if spec_type== 2:
        all_paths_with_basepath = _get_paths_oas2_dict(spec,path)
        return all_paths_with_basepath, spec_type
    elif spec_type == 3:
        all_paths_with_basepath = _get_paths_oas3_dict(spec,path)
        return all_paths_with_basepath, spec_type

# def _get_path_from_spec(spec, path):
#     spec_type = _get_oas_type(spec = spec)
#     if spec_type== 2:
#         return spec.get('paths').get(path), spec_type
#     elif spec_type == 3:
#         return spec.get('paths').get(path), spec_type
    
def _scan_paths_oas3( spec):
    paths = spec.get("paths")
    
    all_paths = paths.keys()
    all_paths_with_basepath = []
    basepath = _get_oas3_basepath(spec)
    for path in all_paths:
        all_paths_with_basepath.append((basepath + path).replace('//','/'))


    return all_paths_with_basepath, all_paths
def deep_compare(obj1, obj2):
    if type(obj1) != type(obj2):
        return False
    
    if isinstance(obj1, dict):
        if obj1.keys()  != obj2.keys():
            return False
        for key in obj1.keys():
            if not deep_compare(obj1[key], obj2[key]):
                return False
        return True

    if isinstance(obj1, list):
        if len(obj1) != len(obj2):
            return False
        for i in range(len(obj1)):
            if not deep_compare(obj1[i], obj2[i]):
                return False
        return True

    return obj1 == obj2


class ReportGenerator:
    def generate_report(self, diff_dict):
        if not len(diff_dict):
            print("No differnces found")
        else:
            print("Differnces")


        
        
# resolve_definitions('source/ext-api.zurichna.com-_papi-discovery.json',{'$ref': '#/definitions/2688960936_coverages'})
# resolve_definitions('target/validateclaimpayment-prcs-api.json',{'$ref': '#/components/schemas/type'},)
        
# resolve_definitions('target/validateclaimpayment-prcs-api.json', {'$ref': '#/components/schemas/paykindCodeDetails'}, '/validateClaimPayment','post')
        # ['string', 'string', 'number', 'string', 'string']

# resolve_definitions('target/validateclaimpayment-prcs-api.json', {'$ref': '#/components/schemas/subClass'}, '/validateClaimPayment','post')
# ['string', 'string']

# resolve_definitions('target/validateclaimpayment-prcs-api.json', {'$ref': '#/components/schemas/valuationSubClasses'}, '/validateClaimPayment','post')
# ['string', 'string', 'number', 'string', 'string', 'string', 'string']


# resolve_definitions('target/validateclaimpayment-prcs-api.json', {'$ref': '#/components/schemas/coverages'}, '/validateClaimPayment','post')

