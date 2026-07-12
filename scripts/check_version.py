import os
import re
import yaml
import json

class VersionSyncChecker:
    def __init__(self, root_dir='.'):
        self.root_dir = root_dir
        self.mandatory_files = ['README.md', 'CHANGELOG.md', 'SPEC.md', 'MEMOIR.md']
        self.version_pattern = r'(\d+)\.(\d+)\.(\d+)'

    def extract_yaml_front_matter(self, content):
        if content.startswith('\ufeff'):
            content = content[1:]

        lines = content.splitlines(keepends=True)
        if not lines:
            return None

        if lines[0].strip() != '---':
            return None

        header_lines = []
        for line in lines[1:]:
            if line.strip() == '---':
                return ''.join(header_lines)
            header_lines.append(line)
        return None

    def parse_version(self, v_str):
        if not v_str: return None
        m = re.search(self.version_pattern, v_str)
        if m:
            return [int(x) for x in m.groups()]
        return None

    def format_version(self, v_list):
        return f"{v_list[0]}.{v_list[1]}.{v_list[2]}"

    def get_sot_version(self):
        changelog_path = os.path.join(self.root_dir, 'CHANGELOG.md')
        if not os.path.exists(changelog_path):
            # Try to find any of the mandatory files to see if we can get a version
            for f_name in self.mandatory_files:
                p = os.path.join(self.root_dir, f_name)
                if os.path.exists(p):
                    with open(p, 'r', encoding='utf-8') as f:
                        content = f.read()
                        header_content = self.extract_yaml_front_matter(content)
                        if header_content is not None:
                            try:
                                data = yaml.safe_load(header_content)
                                v = self.parse_version(data.get('project_version'))
                                if v: return v
                            except: pass
            return None
        
        with open(changelog_path, 'r', encoding='utf-8') as f:
            content = f.read()
            header_content = self.extract_yaml_front_matter(content)
            if header_content is not None:
                try:
                    data = yaml.safe_load(header_content)
                    if 'project_version' in data:
                        v = self.parse_version(data['project_version'])
                        if v: return v
                except:
                    pass
            
            matches = re.findall(r'## \[?' + self.version_pattern + r'\]?', content)
            if matches:
                return [int(x) for x in matches[0]]
        return None

    def check_file_header(self, file_path, expected_version):
        full_path = os.path.join(self.root_dir, file_path)
        if not os.path.exists(full_path):
            return {'status': 'missing_file'}
        
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()
            header_content = self.extract_yaml_front_matter(content)
            if header_content is None:
                return {'status': 'missing_header'}
            
            try:
                data = yaml.safe_load(header_content)
                current_v = self.parse_version(data.get('project_version', ''))
                if not current_v:
                    return {'status': 'invalid_version_in_header', 'header': data}
                
                if current_v != expected_version:
                    return {
                        'status': 'version_mismatch',
                        'current': self.format_version(current_v),
                        'expected': self.format_version(expected_version)
                    }
                return {'status': 'ok', 'version': self.format_version(current_v)}
            except Exception as e:
                return {'status': 'error', 'message': str(e)}

    def check_package_json(self, expected_version):
        path = os.path.join(self.root_dir, 'package.json')
        if not os.path.exists(path):
            return None
        
        with open(path, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
                v_str = data.get('version', '')
                current_v = self.parse_version(v_str)
                if not current_v:
                    return {'status': 'missing_or_invalid_version'}
                
                if current_v != expected_version:
                    return {
                        'status': 'version_mismatch',
                        'current': self.format_version(current_v),
                        'expected': self.format_version(expected_version)
                    }
                return {'status': 'ok', 'version': self.format_version(current_v)}
            except:
                return {'status': 'parse_error'}

    def check_version_file(self, expected_version):
        path = os.path.join(self.root_dir, 'VERSION')
        if not os.path.exists(path):
            return None
        
        with open(path, 'r', encoding='utf-8') as f:
            v_str = f.read().strip()
            current_v = self.parse_version(v_str)
            if not current_v:
                return {'status': 'missing_or_invalid_version'}
            
            if current_v != expected_version:
                return {
                    'status': 'version_mismatch',
                    'current': self.format_version(current_v),
                    'expected': self.format_version(expected_version)
                }
            return {'status': 'ok', 'version': self.format_version(current_v)}

    def run_check(self):
        sot_v = self.get_sot_version()
        if not sot_v:
            return {"error": "Could not determine Source of Truth version"}
        
        expected_str = self.format_version(sot_v)
        results = {
            "expected_version": expected_str,
            "files": {}
        }
        
        for f in self.mandatory_files:
            results["files"][f] = self.check_file_header(f, sot_v)
            
        pkg_res = self.check_package_json(sot_v)
        if pkg_res:
            results["files"]["package.json"] = pkg_res
            
        version_file_res = self.check_version_file(sot_v)
        if version_file_res:
            results["files"]["VERSION"] = version_file_res
            
        return results

if __name__ == "__main__":
    import sys
    root = sys.argv[1] if len(sys.argv) > 1 else '.'
    checker = VersionSyncChecker(root)
    report = checker.run_check()
    print(json.dumps(report, indent=2, ensure_ascii=False))
