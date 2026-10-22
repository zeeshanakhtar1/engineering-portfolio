"""Offline directory backup with SHA256 integrity and safe restore."""
import argparse,hashlib,json,tarfile,time
from pathlib import Path

def checksum(path):
    digest=hashlib.sha256()
    with open(path,'rb') as stream:
        for block in iter(lambda:stream.read(1024*1024),b''):
            digest.update(block)
    return digest.hexdigest()

def snapshot(source,archive):
    source=Path(source).resolve();archive=Path(archive).resolve()
    if not source.is_dir():raise ValueError('backup source must be a directory')
    if archive.is_relative_to(source):raise ValueError('archive must be outside source')
    archive.parent.mkdir(parents=True,exist_ok=True)
    objects=[]
    with tarfile.open(archive,'w:gz') as tar:
        for path in sorted(source.rglob('*')):
            if path.is_symlink():raise ValueError('symlinks not allowed in backup')
            if path.is_file():
                relative=path.relative_to(source).as_posix()
                tar.add(path,arcname=relative,recursive=False)
                objects.append({'path':relative,'sha256':checksum(path),'bytes':path.stat().st_size})
    manifest={'schema':1,'files':objects,'archive_sha256':checksum(archive)}
    archive.with_suffix(archive.suffix+'.manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    return manifest

def restore(archive,destination):
    archive=Path(archive).resolve();destination=Path(destination).resolve()
    manifest=json.loads(archive.with_suffix(archive.suffix+'.manifest.json').read_text(encoding='utf-8'))
    if checksum(archive)!=manifest['archive_sha256']:raise ValueError('backup archive checksum mismatch')
    destination.mkdir(parents=True,exist_ok=True)
    started=time.monotonic()
    files={record['path']:record for record in manifest['files']}
    with tarfile.open(archive,'r:gz') as tar:
        actual={m.name for m in tar.getmembers()}
        if actual!=set(files):raise ValueError('archive contents mismatch manifest')
        for member in tar.getmembers():
            if not member.isfile() or member.name.startswith('/') or '..' in Path(member.name).parts or member.issym() or member.islnk():
                raise ValueError('unsafe archive entry')
            target=(destination/member.name).resolve()
            if not target.is_relative_to(destination):raise ValueError('archive traversal blocked')
            if target.exists():raise ValueError('restore destination must be empty')
            target.parent.mkdir(parents=True,exist_ok=True)
            with tar.extractfile(member) as src,open(target,'wb') as dst:
                for chunk in iter(lambda:src.read(1024*1024),b''):
                    dst.write(chunk)
            if checksum(target)!=files[member.name]['sha256']:
                raise ValueError('restored file integrity mismatch')
    return {'restored_files':len(files),'restore_seconds':round(time.monotonic()-started,3),'verified':True}

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('action',choices=['backup','restore'])
    parser.add_argument('source')
    parser.add_argument('destination')
    opts=parser.parse_args()
    result=snapshot(opts.source,opts.destination) if opts.action=='backup' else restore(opts.source,opts.destination)
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
