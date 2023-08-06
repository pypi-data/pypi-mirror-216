from concurrent.futures import ProcessPoolExecutor
import os
import pickle
import requests

from .serialization import Deserializer
from .utilities import get_auth
from .converters import to_dataframe, metrics_to_dataframe

CONCURRENT_DOWNLOADS = 10
DOWNLOAD_CHUNK_SIZE = 8192
DOWNLOAD_TIMEOUT = 30

def downloader(job):
    """
    Download the specified file to the specified directory
    """
    try:
        response = requests.get(job['url'], stream=True, timeout=DOWNLOAD_TIMEOUT)
    except requests.exceptions.RequestException:
        return

    total_length = response.headers.get('content-length')

    with open(os.path.join(job['path'], job['filename']), 'wb') as fh:
        if total_length is None:
            fh.write(response.content)
        else:
            for data in response.iter_content(chunk_size=DOWNLOAD_CHUNK_SIZE):
                fh.write(data)

class Client(object):
    """
    Class for querying Simvue
    """
    def __init__(self):
        self._url, self._token = get_auth()
        self._headers = {"Authorization": f"Bearer {self._token}"}

    def get_run(self, run, system=False, tags=False, metadata=False):
        """
        Get a single run
        """
        params = {'name': run,
                  'filter': None,
                  'system': system,
                  'tags': tags,
                  'metadata': metadata}

        response = requests.get(f"{self._url}/api/runs", headers=self._headers, params=params)

        if response.status_code == 404:
            if 'detail' in response.json():
                if response.json()['detail'] == 'run does not exist':
                    raise Exception('Run does not exist')

        if response.status_code == 200:
            return response.json()

        raise Exception(response.text)

    def get_runs(self, filters, system=False, tags=False, metadata=False, format='dict'):
        """
        Get runs
        """
        params = {'name': None,
                  'filters': ','.join(filters),
                  'system': system,
                  'tags': tags,
                  'metadata': metadata}

        response = requests.get(f"{self._url}/api/runs", headers=self._headers, params=params)
        response.raise_for_status()

        if response.status_code == 200:
            if format == 'dict':
                return response.json()
            elif format == 'dataframe':
                return to_dataframe(response.json())
            else:
                raise Exception('invalid format specified')

        return None

    def delete_run(self, run):
        """
        Delete run
        """
        params = {'name': run}

        response = requests.delete(f"{self._url}/api/runs", headers=self._headers, params=params)

        if response.status_code == 200:
            if 'runs' in response.json():
                return response.json()['runs']

        raise Exception(response.text)

    def delete_runs(self, folder):
        """
        Delete runs in folder
        """
        params = {'folder': folder}

        response = requests.delete(f"{self._url}/api/runs", headers=self._headers, params=params)

        if response.status_code == 200:
            if 'runs' in response.json():
                return response.json()['runs']

        raise Exception(response.text)

    def delete_folder(self, folder, runs=False):
        """
        Delete folder
        """
        params = {'name': folder,
                  'delete_runs': runs}

        response = requests.delete(f"{self._url}/api/folders", headers=self._headers, params=params)

        if response.status_code == 200:
            if 'runs' in response.json():
                return response.json()['runs']
            return []

        raise Exception(response.text)

    def list_artifacts(self, run, category=None):
        """
        List artifacts associated with a run
        """
        params = {'run': run}
        if category:
            params['category'] = category        

        response = requests.get(f"{self._url}/api/artifacts", headers=self._headers, params=params)

        if response.status_code == 404:
            if 'detail' in response.json():
                if response.json()['detail'] == 'run does not exist':
                    raise Exception('Run does not exist')

        if response.status_code == 200:
            return response.json()

        raise Exception(response.text)

    def get_artifact(self, run, name, allow_pickle=False):
        """
        Return the contents of the specified artifact
        """
        params = {'run': run, 'name': name}

        response = requests.get(f"{self._url}/api/artifacts", headers=self._headers, params=params)

        if response.status_code == 404:
            if 'detail' in response.json():
                if response.json()['detail'] == 'run does not exist':
                    raise Exception('Run does not exist')
                elif response.json()['detail'] == 'artifact does not exist':
                    raise Exception('Artifact does not exist')

        if response.status_code != 200:
            return None

        url = response.json()[0]['url']
        mimetype = response.json()[0]['type']

        response = requests.get(url, timeout=DOWNLOAD_TIMEOUT)
        response.raise_for_status()

        content = Deserializer().deserialize(response.content, mimetype, allow_pickle)
        if content is not None:
            return content

        return response.content

    def get_artifact_as_file(self, run, name, path='./'):
        """
        Download an artifact
        """
        params = {'run': run, 'name': name}

        response = requests.get(f"{self._url}/api/artifacts", headers=self._headers, params=params)

        if response.status_code == 404:
            if 'detail' in response.json():
                if response.json()['detail'] == 'run does not exist':
                    raise Exception('Run does not exist')
                elif response.json()['detail'] == 'artifact does not exist':
                    raise Exception('Artifact does not exist')

        if response.status_code == 200:
            if response.json():
                url = response.json()[0]['url']
                downloader({'url': url,
                            'filename': os.path.basename(name),
                            'path': path})

        else:
            raise Exception(response.text)

    def get_artifacts_as_files(self,
                               run,
                               path=None,
                               category=None,
                               startswith=None,
                               contains=None,
                               endswith=None):
        """
        Get artifacts associated with a run & save as files
        """
        params = {'run': run}
        if category:
            params['category'] = category

        response = requests.get(f"{self._url}/api/artifacts", headers=self._headers, params=params)

        if response.status_code == 404:
            if 'detail' in response.json():
                if response.json()['detail'] == 'run does not exist':
                    raise Exception('Run does not exist')

        if not path:
            path = './'

        if response.status_code == 200:
            downloads = []
            for item in response.json():
                if startswith:
                    if not item['name'].startswith(startswith):
                        continue
                if contains:
                    if contains not in item['name']:
                        continue
                if endswith:
                    if not item['name'].endswith(endswith):
                        continue

                job = {}
                job['url'] = item['url']
                job['filename'] = os.path.basename(item['name'])
                job['path'] = os.path.join(path, os.path.dirname(item['name']))

                if os.path.isfile(os.path.join(job['path'], job['filename'])):
                    continue

                if job['path']:
                    os.makedirs(job['path'], exist_ok=True)
                else:
                    job['path'] = path
                downloads.append(job)

            with ProcessPoolExecutor(CONCURRENT_DOWNLOADS) as executor:
                for item in downloads:
                    executor.submit(downloader, item)

        else:
            raise Exception(response.text)

    def get_folder(self, folder, tags=False, metadata=False):
        """
        Get a single folder
        """
        params = {'name': folder,
                  'tags': tags,
                  'metadata': metadata}

        response = requests.get(f"{self._url}/api/folders", headers=self._headers, params=params)

        if response.status_code == 404:
            if 'detail' in response.json():
                if response.json()['detail'] == 'no such folder':
                    raise Exception('Folder does not exist')

        if response.status_code == 200:
            return response.json()

        raise Exception(response.text)

    def get_folders(self, filters, tags=False, metadata=False):
        """
        Get folders
        """
        params = {'filters': ','.join(filters),
                  'tags': tags,
                  'metadata': metadata}

        response = requests.get(f"{self._url}/api/folders", headers=self._headers, params=params)

        if response.status_code == 200:
            return response.json()

        raise Exception(response.text)
        
    def get_metrics_names(self, run):
        """
        Return a list of metrics names
        """
        params = {'runs': run,
                  'timeseries': False}

        response = requests.get(f"{self._url}/api/metrics", headers=self._headers, params=params)

        if response.status_code == 200:
            return response.json()

        raise Exception(response.text)     

    def get_metrics_summaries(self, run, name):
        """
        Get summary metrics for the specified run and metrics name
        """
        params = {'runs': run,
                  'metrics': name,
                  'summary': True}

        response = requests.get(f"{self._url}/api/metrics", headers=self._headers, params=params)

        if response.status_code == 200:
            return response.json()

        raise Exception(response.text)

    def get_metrics(self, run, name, xaxis, format='list'):
        """
        Get time series metrics for the specified run and metrics name
        """
        params = {'runs': run,
                  'metrics': name,
                  'summary': False,
                  'xaxis': xaxis}

        if xaxis not in ('step', 'time', 'timestamp'):
            raise Exception('Invalid xaxis specified, should be either "step", "time", or "timestamp"')

        if format not in ('list', 'dataframe'):
            raise Exception('Invalid format specified, should be either "list" or "dataframe"')

        response = requests.get(f"{self._url}/api/metrics", headers=self._headers, params=params)

        if response.status_code == 200:
            if format == 'dataframe':
                return metrics_to_dataframe(response.json(), xaxis, name=name)
            return response.json()

        raise Exception(response.text)

    def get_metrics_multiple(self, runs, names, xaxis, sample_by=0, format='list'):
        """
        Get time series metrics from multiple runs and/or metrics
        """
        params = {'runs': ','.join(runs),
                  'metrics': ','.join(names),
                  'summary': False,
                  'sample_by': sample_by,
                  'xaxis': xaxis}

        if xaxis not in ('step', 'time'):
            raise Exception('Invalid xaxis specified, should be either "step" or "time"')

        if format not in ('list', 'dataframe'):
            raise Exception('Invalid format specified, should be either "list" or "dataframe"')

        response = requests.get(f"{self._url}/api/metrics", headers=self._headers, params=params)

        if response.status_code == 200:
            if format == 'dataframe':
                return metrics_to_dataframe(response.json(), xaxis)
            return response.json()

        raise Exception(response.text)
        
    def plot_metrics(self, runs, names, xaxis, sample_by=0):
        """
        Plot time series metrics from multiple runs and/or metrics
        """
        data = self.get_metrics_multiple(runs, names, xaxis, sample_by, format='dataframe')

        import matplotlib.pyplot as plt

        for run in runs:
            for name in names:
                label = None
                if len(runs) > 1 and len(names) > 1:
                    label = f"{run}: {name}"
                elif len(runs) > 1 and len(names) == 1:
                    label = run
                elif len(runs) == 1 and len(names) > 1:
                    label = name

                plt.plot(data[(run, name, xaxis)],
                         data[(run, name, 'value')],
                         label=label)

        if xaxis == 'step':
            plt.xlabel('steps')
        elif xaxis == 'time':
            plt.xlabel('relative time')

        if len(names) == 1:
            plt.ylabel(names[0])

        return plt       

    def get_events(self, run, filter=None, start=0, num=0):
        """
        Return events from the specified run
        """
        params = {'run': run,
                  'filter': filter,
                  'start': start,
                  'num': num}

        response = requests.get(f"{self._url}/api/events", headers=self._headers, params=params)

        if response.status_code == 200:
            return response.json()

        raise Exception(response.text)
