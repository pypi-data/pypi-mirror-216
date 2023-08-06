'''
Modul utama pypipr yang berisi semua yg ada dalam pypipr
'''


from .lib import *
from .console import *
from .engineering import *
from .uncategorize import *


"""
Variabel yang digunakan dalam function
format variabel: __[function]__[var_name]__
"""
# is_empty()
__is_empty__empty_list__ = [None, False, 0, -0]
__is_empty__empty_list__ += ["0", "", "-0", "\n", "\t"]
__is_empty__empty_list__ += [set(), dict(), list(), tuple()]
# batchmaker()
__batchmaker__regex_pattern__ = r"{(?:[^a-zA-Z0-9{}]+)?([a-zA-Z]|\d+)[^a-zA-Z0-9{}]+([a-zA-Z]|\d+)(?:[^a-zA-Z0-9{}]+(\d+))?(?:[^a-zA-Z0-9{}]+)?}"
__batchmaker__regex_compile__ = re.compile(__batchmaker__regex_pattern__)
# is_valid_url()
__is_valid_url__pattern__ = "^(?:(?:(?:https?|ftp):)?\/\/)(?:\S+(?::\S*)?@)?(?:(?!(?:10|127)(?:\.\d{1,3}){3})(?!(?:169\.254|192\.168)(?:\.\d{1,3}){2})(?!172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))|(?:(?:[a-z0-9\u00a1-\uffff][a-z0-9\u00a1-\uffff_-]{0,62})?[a-z0-9\u00a1-\uffff]\.)+(?:[a-z\u00a1-\uffff]{2,}\.?))(?::\d{2,5})?(?:[/?#]\S*)?$"
__is_valid_url__regex__ = re.compile(__is_valid_url__pattern__, flags=re.IGNORECASE)


class generator:
    """
    Class ini menyediakan beberapa fungsi yang bisa mengembalikan generator.
    Digunakan untuk mengoptimalkan program.

    Class ini dibuat karena python generator yang disimpan dalam variabel
    hanya dapat diakses satu kali.
    """

    @staticmethod
    def iscandir(
        folder_name=".",
        glob_pattern="*",
        recursive=True,
        scan_file=True,
        scan_folder=True,
    ):
        """
        Mempermudah scandir untuk mengumpulkan folder dan file.

        ```python
        print(generator.iscandir())
        print(iscandir("./", recursive=False, scan_file=False))
        ```
        """
        path_obj = pathlib.Path(folder_name)
        if recursive:
            path_obj = path_obj.rglob(glob_pattern)
        else:
            path_obj = path_obj.glob(glob_pattern)

        for i in path_obj:
            if scan_folder and i.is_dir():
                yield i
            if scan_file and i.is_file():
                yield i

    @staticmethod
    def get_class_method(cls):
        """
        Mengembalikan berupa tuple yg berisi list dari method dalam class

        ```python
        class ExampleGetClassMethod:
            def a():
                return [x for x in range(10)]

            def b():
                return [x for x in range(10)]

            def c():
                return [x for x in range(10)]

            def d():
                return [x for x in range(10)]

        print(get_class_method(ExampleGetClassMethod))
        ```
        """
        for x in dir(cls):
            a = getattr(cls, x)
            if not x.startswith("__") and callable(a):
                yield a

    @staticmethod
    def chunck_array(array, size, start=0):
        """
        Membagi array menjadi potongan-potongan dengan besaran yg diinginkan

        ```python
        array = [2, 3, 12, 3, 3, 42, 42, 1, 43, 2, 42, 41, 4, 24, 32, 42, 3, 12, 32, 42, 42]
        print(generator.chunck_array(array, 5))
        print(chunck_array(array, 5))
        ```
        """
        for i in range(start, len(array), size):
            yield array[i : i + size]

    @staticmethod
    def irange(start, finish, step=1):
        """
        Meningkatkan fungsi range() dari python untuk pengulangan menggunakan huruf

        ```python
        print(generator.irange('a', 'c'))
        print(irange('z', 'a', 10))
        print(irange('a', 'z', 10))
        print(irange(1, '7'))
        print(irange(10, 5))
        ```
        """

        def casting_class():
            start_int = isinstance(start, int)
            finish_int = isinstance(finish, int)
            start_str = isinstance(start, str)
            finish_str = isinstance(finish, str)
            start_numeric = start.isnumeric() if start_str else False
            finish_numeric = finish.isnumeric() if finish_str else False

            if start_numeric and finish_numeric:
                # irange("1", "5")
                return (int, str)

            if (start_numeric or start_int) and (finish_numeric or finish_int):
                # irange("1", "5")
                # irange("1", 5)
                # irange(1, "5")
                # irange(1, 5)
                return (int, int)

            if start_str and finish_str:
                # irange("a", "z")
                # irange("p", "g")
                return (ord, chr)

            """
            kedua if dibawah ini sudah bisa berjalan secara logika, tetapi
            perlu dimanipulasi supaya variabel start dan finish bisa diubah.
            """
            # irange(1, 'a') -> irange('1', 'a')
            # irange(1, '5') -> irange(1, 5)
            # irange('1', 5) -> irange(1, 5)
            # irange('a', 5) -> irange('a', '5')
            #
            # if start_str and finish_int:
            #     # irange("a", 5) -> irange("a", "5")
            #     finish = str(finish)
            #     return (ord, chr)
            #
            # if start_int and finish_str:
            #     # irange(1, "g") -> irange("1", "g")
            #     start = str(start)
            #     return (ord, chr)

            raise Exception(
                f"[{start} - {finish}] tidak dapat diidentifikasi kesamaannya"
            )

        counter_class, converter_class = casting_class()
        start = counter_class(start)
        finish = counter_class(finish)

        step = 1 if is_empty(step) else int(step)

        faktor = 1 if finish > start else -1
        step *= faktor
        finish += faktor

        for i in range(start, finish, step):
            yield converter_class(i)

    @staticmethod
    def sets_ordered(iterator):
        """
        Hanya mengambil nilai unik dari suatu list

        ```python
        array = [2, 3, 12, 3, 3, 42, 42, 1, 43, 2, 42, 41, 4, 24, 32, 42, 3, 12, 32, 42, 42]
        print(generator.sets_ordered(array))
        print(sets_ordered(array))
        ```
        """
        for i in dict.fromkeys(iterator):
            yield i

    @staticmethod
    def filter_empty(iterable, zero_is_empty=True, str_strip=True):
        for i in iterable:
            if i == 0 and zero_is_empty:
                continue
            if isinstance(i, str) and str_strip:
                i = i.strip()
            if not is_iterable(i) and not to_str(i):
                continue
            yield i

    @staticmethod
    def batchmaker(text: str):
        """
        Alat Bantu untuk membuat teks yang berulang.
        Gunakan {[start][separator][finish]([separator][step])}.
        ```
        [start] dan [finish]    -> bisa berupa huruf maupun angka
        ([separator][step])     -> bersifat optional
        [separator]             -> selain huruf dan angka
        [step]                  -> berupa angka positif
        ```

        ```python
        s = "Urutan {1/6/3} dan {10:9} dan {j k} dan {Z - A - 15} saja."
        print(generator.batchmaker(s))
        print(batchmaker(s))
        ```
        """
        s = __batchmaker__regex_compile__.search(text)
        if s is None:
            yield text
            return

        find = s.group()
        start, finish, step = s.groups()

        for i in generator.irange(start, finish, step):
            r = text.replace(find, i, 1)
            yield from generator.batchmaker(r)


def print_colorize(
    text,
    color=colorama.Fore.GREEN,
    bright=colorama.Style.BRIGHT,
    color_end=colorama.Style.RESET_ALL,
    text_start="",
    text_end="\n",
):
    """
    Print text dengan warna untuk menunjukan text penting

    ```py
    print_colorize("Print some text")
    print_colorize("Print some text", color=colorama.Fore.RED)
    ```
    """
    print(f"{text_start}{color + bright}{text}{color_end}", end=text_end, flush=True)


def log(text=None):
    """
    Decorator untuk mempermudah pembuatan log karena tidak perlu mengubah fungsi yg sudah ada.
    Melakukan print ke console untuk menginformasikan proses yg sedang berjalan didalam program.

    ```py
    @log
    def some_function():
        pass

    @log()
    def some_function_again():
        pass

    @log("Calling some function")
    def some_function_more():
        pass

    some_function()
    some_function_again()
    some_function_more()
    ```
    """

    def inner_log(func=None):
        def callable_func(*args, **kwargs):
            main_function(text)
            result = func(*args, **kwargs)
            return result

        def main_function(param):
            print_log(param)

        if func is None:
            return main_function(text)
        return callable_func

    if text is None:
        return inner_log
    elif callable(text):
        return inner_log(text)
    else:
        # inner_log(None)
        return inner_log


def print_log(text):
    """
    Akan melakukan print ke console.
    Berguna untuk memberikan informasi proses program yg sedang berjalan.

    ```py
    print_log("Standalone Log")
    ```
    """
    print_colorize(f">>> {text}")


def console_run(info, command=None, print_info=True, capture_output=False):
    """
    Menjalankan command seperti menjalankan command di Command Terminal

    ```py
    console_run('dir')
    console_run('ls')
    ```
    """
    if command is None:
        command = info

    if print_info:
        print_log(info)

    param = dict(shell=True)
    if capture_output:
        param |= dict(capture_output=True, text=True)

    return subprocess.run(command, **param)


def input_char(
    prompt=None,
    prompt_ending="",
    newline_after_input=True,
    echo_char=True,
    default=None,
):
    """
    Meminta masukan satu huruf tanpa menekan Enter.

    ```py
    input_char("Input char : ")
    input_char("Input char : ", default='Y')
    input_char("Input Char without print : ", echo_char=False)
    ```
    """
    if prompt:
        print(prompt, end=prompt_ending, flush=True)
    
    if default is not None:
        a = default
    else:
        a = _getch.getche() if echo_char else _getch.getch()
    
    if newline_after_input:
        print()

    if WINDOWS:
        return a.decode()
    if LINUX:
        return a
    raise Exception('Platform tidak didukung.')


def datetime_now(timezone=None):
    """
    Memudahkan dalam membuat Datetime untuk suatu timezone tertentu

    ```python
    print(datetime_now("Asia/Jakarta"))
    print(datetime_now("GMT"))
    print(datetime_now("Etc/GMT+7"))
    ```
    """
    tz = zoneinfo.ZoneInfo(timezone) if timezone else None
    return datetime.datetime.now(tz)


def datetime_from_string(iso_string, timezone="UTC"):
    """
    Parse iso_string menjadi datetime object

    ```python
    print(datetime_from_string("2022-12-12 15:40:13").isoformat())
    print(datetime_from_string("2022-12-12 15:40:13", timezone="Asia/Jakarta").isoformat())
    ```
    """
    return datetime.datetime.fromisoformat(iso_string).replace(
        tzinfo=zoneinfo.ZoneInfo(timezone)
    )


def sets_ordered(iterable):
    return type(iterable)(generator.sets_ordered(iterable))


def chunck_array(array, size, start=0):
    return tuple(generator.chunck_array(array=array, size=size, start=start))


def github_push(commit=None):
    """
    Menjalankan command status, add, commit dan push

    ```py
    github_push('Commit Message')
    ```
    """

    def console_input(prompt, default):
        print_colorize(prompt, text_end="")
        if default:
            print(default)
            return default
        else:
            return input()

    print_log("Menjalankan Github Push")
    console_run("Checking files", "git status")
    msg = console_input("Commit Message if any or empty to exit : ", commit)
    if msg:
        console_run("Mempersiapkan files", "git add .")
        console_run("Menyimpan files", f'git commit -m "{msg}"')
        console_run("Mengirim files", "git push")
    print_log("Selesai Menjalankan Github Push")


def github_pull():
    """
    Menjalankan command `git pull`

    ```py
    github_pull()
    ```
    """
    console_run("Git Pull", "git pull")


def create_folder(folder_name):
    """
    Membuat folder.
    Membuat folder secara recursive dengan permission.

    ```py
    create_folder("contoh_membuat_folder")
    create_folder("contoh/membuat/folder/recursive")
    create_folder("./contoh_membuat_folder/secara/recursive")
    ```
    """
    pathlib.Path(folder_name).mkdir(parents=True, exist_ok=True)


def iscandir(
    folder_name=".",
    glob_pattern="*",
    recursive=True,
    scan_file=True,
    scan_folder=True,
):
    return tuple(
        generator.iscandir(
            folder_name=folder_name,
            glob_pattern=glob_pattern,
            recursive=recursive,
            scan_file=scan_file,
            scan_folder=scan_folder,
        )
    )


def get_filesize(filename):
    """
    Mengambil informasi file size dalam bytes

    ```python
    print(get_filesize(__file__))
    ```
    """
    return os.stat(filename).st_size


def get_filemtime(filename):
    """
    Mengambil informasi last modification time file dalam nano seconds

    ```python
    print(get_filemtime(__file__))
    ```
    """
    return os.stat(filename).st_mtime_ns


def dict_first(d: dict, remove=False):
    """
    Mengambil nilai (key, value) pertama dari dictionary dalam bentuk tuple.

    ```python
    d = {
        "key2": "value2",
        "key3": "value3",
        "key1": "value1",
    }
    print(dict_first(d, remove=True))
    print(dict_first(d))
    ```
    """
    for k in d:
        return (k, d.pop(k) if remove else d[k])


def random_bool():
    """
    Menghasilkan nilai random True atau False.
    Fungsi ini merupakan fungsi tercepat untuk mendapatkan random bool.
    Fungsi ini sangat cepat, tetapi pemanggilan fungsi ini membutuhkan
    overhead yg besar.

    ```python
    print(random_bool())
    ```
    """
    return bool(random.getrandbits(1))


def set_timeout(interval, func, args=None, kwargs=None):
    """
    Menjalankan fungsi ketika sudah sekian detik.
    Apabila timeout masih berjalan tapi kode sudah selesai dieksekusi semua, maka
    program tidak akan berhenti sampai timeout selesai, kemudian fungsi dijalankan,
    kemudian program dihentikan.

    ```python
    set_timeout(3, lambda: print("Timeout 3"))
    x = set_timeout(7, lambda: print("Timeout 7"))
    print(x)
    print("menghentikan timeout 7")
    x.cancel()
    ```
    """
    t = threading.Timer(interval=interval, function=func, args=args, kwargs=kwargs)
    t.start()
    # t.cancel() untuk menghentikan timer sebelum waktu habis
    return t


def get_class_method(cls):
    return tuple(generator.get_class_method(cls))


class ComparePerformance:
    """
    Menjalankan seluruh method dalam class,
    Kemudian membandingkan waktu yg diperlukan.
    Nilai 100 berarti yang tercepat.

    ```python
    class ExampleComparePerformance(ComparePerformance):
        # number = 1
        z = 10

        def a(self):
            return (x for x in range(self.z))

        def b(self):
            return tuple(x for x in range(self.z))

        def c(self):
            return [x for x in range(self.z)]

        def d(self):
            return list(x for x in range(self.z))

    pprint.pprint(ExampleComparePerformance().compare_result(), depth=100)
    print(ExampleComparePerformance().compare_performance())
    print(ExampleComparePerformance().compare_performance())
    print(ExampleComparePerformance().compare_performance())
    print(ExampleComparePerformance().compare_performance())
    print(ExampleComparePerformance().compare_performance())
    ```
    """

    number = 1

    def get_all_instance_methods(self):
        c = set(dir(__class__))
        l = (x for x in dir(self) if x not in c)
        return tuple(
            x for x in l if callable(getattr(self, x)) and not x.startswith("_")
        )

    def test_method_performance(self, methods):
        d = {x: [] for x in methods}
        for _ in range(self.number):
            for i in set(methods):
                d[i].append(self.get_method_performance(i))
        return d

    def get_method_performance(self, callable_method):
        c = getattr(self, callable_method)
        s = time.perf_counter_ns()
        for _ in range(self.number):
            c()
        f = time.perf_counter_ns()
        return f - s

    def calculate_average(self, d: dict):
        r1 = {i: avg(v) for i, v in d.items()}
        min_value = min(r1.values())
        persen = lambda v: int(v / min_value * 100)
        r2 = {i: persen(v) for i, v in r1.items()}
        return r2

    def compare_performance(self):
        m = self.get_all_instance_methods()
        p = self.test_method_performance(m)
        a = self.calculate_average(p)
        return a

    def compare_result(self):
        m = self.get_all_instance_methods()
        return {x: getattr(self, x)() for x in m}


class RunParallel:
    """
    Menjalankan program secara bersamaan.

    - `class RunParallel` didesain hanya untuk pemrosesan data saja.
    - Penggunaannya `class RunParallel` dengan cara membuat instance sub class beserta data yg akan diproses, kemudian panggil fungsi yg dipilih `run_asyncio / run_multi_threading / run_multi_processing`, kemudian dapatkan hasilnya.
    - `class RunParallel` tidak didesain untuk menyimpan data, karena setiap module terutama module `multiprocessing` tidak dapat mengakses data kelas dari proses yg berbeda.
    - Semua methods akan dijalankan secara paralel kecuali method dengan nama yg diawali underscore `_`
    - Method untuk multithreading/multiprocessing harus memiliki 2 parameter, yaitu: `result: dict` dan `q: queue.Queue`. Parameter `result` digunakan untuk memberikan return value dari method, dan Parameter `q` digunakan untuk mengirim data antar proses.
    - Method untuk asyncio harus menggunakan keyword `async def`, dan untuk perpindahan antar kode menggunakan `await asyncio.sleep(0)`, dan keyword `return` untuk memberikan return value.
    - Return Value berupa dictionary dengan key adalah nama function, dan value adalah return value dari setiap fungsi
    - Menjalankan Multiprocessing harus berada dalam blok `if __name__ == "__main__":` karena area global pada program akan diproses lagi. Terutama pada sistem operasi windows.
    - `run_asyncio()` akan menjalankan kode dalam satu program, hanya saja alur program dapat berpindah-pindah menggunkan `await asyncio.sleep(0)`.
    - `run_multi_threading()` akan menjalankan program dalam satu CPU, hanya saja dalam thread yang berbeda. Walaupun tidak benar-benar berjalan secara bersamaan namun bisa meningkatkan kecepatan penyelesaian program, dan dapat saling mengakses resource antar program.  Akses resource antar program bisa secara langsung maupun menggunakan parameter yang sudah disediakan yaitu `result: dict` dan `q: queue.Queue`.
    - `run_multi_processing()` akan menjalankan program dengan beberapa CPU. Program akan dibuatkan environment sendiri yang terpisah dari program induk. Keuntungannya adalah program dapat benar-benar berjalan bersamaan, namun tidak dapat saling mengakses resource secara langsung. Akses resource menggunakan parameter yang sudah disediakan yaitu `result: dict` dan `q: queue.Queue`.

    ```python
    class ExampleRunParallel(RunParallel):
        z = "ini"

        def __init__(self) -> None:
            self.pop = random.randint(0, 100)

        def _set_property_here(self, v):
            self.prop = v

        def a(self, result: dict, q: queue.Queue):
            result["z"] = self.z
            result["pop"] = self.pop
            result["a"] = "a"
            q.put("from a 1")
            q.put("from a 2")

        def b(self, result: dict, q: queue.Queue):
            result["z"] = self.z
            result["pop"] = self.pop
            result["b"] = "b"
            result["q_get"] = q.get()

        def c(self, result: dict, q: queue.Queue):
            result["z"] = self.z
            result["pop"] = self.pop
            result["c"] = "c"
            result["q_get"] = q.get()

        async def d(self):
            print("hello")
            await asyncio.sleep(0)
            print("hello")

            result = {}
            result["z"] = self.z
            result["pop"] = self.pop
            result["d"] = "d"
            return result

        async def e(self):
            print("world")
            await asyncio.sleep(0)
            print("world")

            result = {}
            result["z"] = self.z
            result["pop"] = self.pop
            result["e"] = "e"
            return result

    if __name__ == "__main__":
        print(ExampleRunParallel().run_asyncio())
        print(ExampleRunParallel().run_multi_threading())
        print(ExampleRunParallel().run_multi_processing())
    ```
    """

    def get_all_instance_methods(self, coroutine):
        c = set(dir(__class__))
        l = (x for x in dir(self) if x not in c)
        return tuple(
            a
            for x in l
            if callable(a := getattr(self, x))
            and not x.startswith("_")
            and asyncio.iscoroutinefunction(a) == coroutine
        )

    def run_asyncio(self):
        m = self.get_all_instance_methods(coroutine=True)
        a = self.module_asyncio(*m)
        return self.dict_results(m, a)

    def run_multi_threading(self):
        m = self.get_all_instance_methods(coroutine=False)
        a = self.module_threading(*m)
        return self.dict_results(m, a)

    def run_multi_processing(self):
        m = self.get_all_instance_methods(coroutine=False)
        a = self.module_multiprocessing(*m)
        return self.dict_results(m, a)

    def dict_results(self, names, results):
        return dict(zip((x.__name__ for x in names), results))

    def module_asyncio(self, *args):
        async def main(*args):
            return await asyncio.gather(*(x() for x in args))

        return asyncio.run(main(*args))

    def module_threading(self, *args):
        a = tuple(dict() for _ in args)
        q = queue.Queue()
        r = tuple(
            threading.Thread(target=v, args=(a[i], q)) for i, v in enumerate(args)
        )
        for i in r:
            i.start()
        for i in r:
            i.join()
        return a

    def module_multiprocessing(self, *args):
        m = multiprocessing.Manager()
        q = m.Queue()
        a = tuple(m.dict() for _ in args)
        r = tuple(
            multiprocessing.Process(target=v, args=(a[i], q))
            for i, v in enumerate(args)
        )
        for i in r:
            i.start()
        for i in r:
            i.join()
        return (i.copy() for i in a)


def avg(i):
    """
    Simple Average Function karena tidak disediakan oleh python

    ```python
    n = [1, 22, 2, 3, 13, 2, 123, 12, 31, 2, 2, 12, 2, 1]
    print(avg(n))
    ```
    """
    return sum(i) / len(i)


def exit_if_empty(*args):
    """
    Keluar dari program apabila seluruh variabel
    setara dengan empty

    ```py
    var1 = None
    var2 = '0'
    exit_if_empty(var1, var2)
    ```
    """
    for i in args:
        if not is_empty(i):
            return
    sys.exit()


def implode(
    iterable,
    separator="",
    start="",
    end="",
    remove_empty=False,
    recursive=True,
    recursive_flat=False,
    str_strip=False,
):
    """
    Simplify Python join functions like PHP function.
    Iterable bisa berupa sets, tuple, list, dictionary.

    ```python
    arr = {'asd','dfs','weq','qweqw'}
    print(implode(arr, ', '))

    arr = '/ini/path/seperti/url/'.split('/')
    print(implode(arr, ','))
    print(implode(arr, ',', remove_empty=True))

    arr = {'a':'satu', 'b':(12, 34, 56), 'c':'tiga', 'd':'empat'}
    print(implode(arr, separator='</li>\\n<li>', start='<li>', end='</li>', recursive_flat=True))
    print(implode(arr, separator='</div>\\n<div>', start='<div>', end='</div>'))
    print(implode(10, ' '))
    ```
    """
    if not is_iterable(iterable):
        iterable = [iterable]

    separator = to_str(separator)

    if isinstance(iterable, dict):
        iterable = iterable.values()

    if remove_empty:
        iterable = (i for i in generator.filter_empty(iterable))

    if recursive:
        rec_flat = dict(start=start, end=end)
        if recursive_flat:
            rec_flat = dict(start="", end="")
        rec = lambda x: implode(
            iterable=x,
            separator=separator,
            **rec_flat,
            remove_empty=remove_empty,
            recursive=recursive,
            recursive_flat=recursive_flat,
        )
        iterable = ((rec(i) if is_iterable(i) else i) for i in iterable)

    iterable = (str(i) for i in iterable)

    if str_strip:
        iterable = (i.strip() for i in iterable)

    result = start

    for index, value in enumerate(iterable):
        if index:
            result += separator
        result += value

    result += end

    return result


def strtr(
    string: str,
    replacements: dict,
    flags=re.DOTALL | re.MULTILINE | re.IGNORECASE,
):
    """
    STRing TRanslate mengubah string menggunakan kamus dari dict.
    Replacement dapat berupa text biasa ataupun regex pattern.
    Apabila replacement berupa regex, gunakan raw string `r"..."`
    Untuk regex capturing gunakan `(...)`, dan untuk mengaksesnya gunakan `\\1`, `\\2`, .., dst.

    ```python
    text = 'aku ini mau ke sini'
    replacements = {
        "sini": "situ",
        r"(ini)": r"itu dan \\1",
    }
    print(strtr(text, replacements))
    ```
    """
    for i, v in replacements.items():
        string = re.sub(i, v, string, flags=flags)
    return string


def print_dir(var, colorize=True):
    """
    Print property dan method yang tersedia pada variabel

    ```python
    p = pathlib.Path("https://www.google.com/")
    print_dir(p, colorize=False)
    ```
    """
    d = dir(var)
    m = max(len(i) for i in d)
    for i in d:
        try:
            a = getattr(var, i)
            r = a() if callable(a) else a
            if colorize:
                color = colorama.Fore.GREEN
                if is_empty(r):
                    color = colorama.Fore.LIGHTRED_EX
                if i.startswith("__"):
                    color = colorama.Fore.CYAN
                print_colorize(f"{i: >{m}}", text_end=" : ", color=color)
                print(r)
            else:
                print(f"{i: >{m}} : {r}")
        except:
            pass


def is_iterable(var, str_is_iterable=False):
    """
    Mengecek apakah suatu variabel bisa dilakukan forloop atau tidak

    ```python
    s = 'ini string'
    print(is_iterable(s))

    l = [12,21,2,1]
    print(is_iterable(l))

    r = range(100)
    print(is_iterable(r))

    d = {'a':1, 'b':2}
    print(is_iterable(d.values()))
    ```
    """

    """ Metode #1 """
    # TYPE_NONE = type(None)
    # TYPE_GENERATOR = type(i for i in [])
    # TYPE_RANGE = type(range(0))
    # TYPE_DICT_VALUES = type(dict().values())
    # it = (list, tuple, set, dict)
    # it += (TYPE_GENERATOR, TYPE_RANGE, TYPE_DICT_VALUES)
    # return isinstance(var, it)

    """ Metode #2 """
    if isinstance(var, str) and not str_is_iterable:
        return False
    # return isinstance(var, collections.abc.Iterable)

    """ Metode #3 """
    try:
        iter(var)
        return True
    except:
        return False


def irange(start, finish, step=1):
    """
    Improve python range() function untuk pengulangan menggunakan huruf

    ```python
    print(generator.irange('a', 'z'))
    print(irange('H', 'a'))
    print(irange('1', '5', 3))
    print(irange('1', 5, 3))
    # print(irange('a', 5, 3))
    print(irange(-10, 4, 3))
    print(irange(1, 5))
    ```
    """
    return list(generator.irange(start, finish, step))


def serialize(data, syntax="yaml", indent=4):
    """
    Mengubah variabel data menjadi string untuk yang dapat dibaca untuk disimpan.
    String yang dihasilkan berbentuk syntax YAML/JSON/HTML.

    ```python
    data = {
        'a': 123,
        't': ['disini', 'senang', 'disana', 'senang'],
        'l': (12, 23, [12, 42]),
    }
    print(serialize(data))
    print(serialize(data, syntax='html'))
    ```
    """
    if syntax == "yaml":
        return yaml.dump(data, indent=indent)
    if syntax == "json":
        return json.dumps(data, indent=indent)
    if syntax == "html":
        return serialize_html(data, indent=indent)
    raise Exception(f"Syntax tidak didukung {syntax}")


def unserialize(data):
    """
    Mengubah string data hasil dari serialize menjadi variabel.
    String data adalah berupa syntax YAML.

    ```python
    data = {
        'a': 123,
        't': ['disini', 'senang', 'disana', 'senang'],
        'l': (12, 23, [12, 42])
    }
    s = serialize(data)
    print(unserialize(s))
    ```
    """
    return yaml.safe_load(data)


def basename(path):
    """
    Mengembalikan nama file dari path

    ```python
    print(basename("/ini/nama/folder/ke/file.py"))
    ```
    """
    return os.path.basename(path)


def dirname(path):
    """
    Mengembalikan nama folder dari path.
    Tanpa trailing slash di akhir.

    ```python
    print(dirname("/ini/nama/folder/ke/file.py"))
    ```
    """
    return os.path.dirname(path)


def batchmaker(text: str):
    return tuple(generator.batchmaker(text))


def filter_empty(iterable, zero_is_empty=True, str_strip=True):
    return type(iterable)(
        generator.filter_empty(
            iterable=iterable,
            zero_is_empty=zero_is_empty,
            str_strip=str_strip,
        )
    )


def to_str(value):
    """
    Mengubah value menjadi string literal

    ```python
    print(to_str(5))
    print(to_str([]))
    print(to_str(False))
    print(to_str(True))
    print(to_str(None))
    ```
    """
    if isinstance(value, str):
        return value
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, bool):
        return "1" if value else "0"
    if is_empty(value):
        return ""
    try:
        return str(value)
    except:
        raise Exception(f"Tipe data {value} tidak diketahui")


def is_empty(variable, empty=__is_empty__empty_list__):
    """
    Mengecek apakah variable setara dengan nilai kosong pada empty.

    Pengecekan nilai yang setara menggunakan simbol '==', sedangkan untuk
    pengecekan lokasi memory yang sama menggunakan keyword 'is'

    ```python
    print(is_empty("teks"))
    print(is_empty(True))
    print(is_empty(False))
    print(is_empty(None))
    print(is_empty(0))
    print(is_empty([]))
    ```
    """
    for e in empty:
        if variable == e:
            return True
    return False


def explode(text, separator="", include_separator=False):
    """
    Memecah text menjadi list berdasarkan separator.

    ```python
    t = '/ini/contoh/path/'
    print(explode(t, separator='/'))
    ```
    """
    if include_separator:
        separator = f"({separator})"

    result = re.split(separator, text, flags=re.IGNORECASE | re.MULTILINE)

    return result


def calculate(teks):
    """
    Mengembalikan hasil dari perhitungan teks menggunakan modul pint.
    Mendukung perhitungan matematika dasar dengan satuan.

    Return value:
    - Berupa class Quantity dari modul pint

    Format:
    - f"{result:~P}"            -> pretty
    - f"{result:~H}"            -> html
    - result.to_base_units()    -> SI
    - result.to_compact()       -> human readable

    ```python
    fx = "3 meter * 10 cm * 3 km"
    res = calculate(fx)
    print(res)
    print(res.to_base_units())
    print(res.to_compact())
    print(f"{res:~P}")
    print(f"{res:~H}")
    ```
    """
    return PintUregQuantity(teks)


def iexec(python_syntax, import_pypipr=True):
    """
    improve exec() python function untuk mendapatkan outputnya

    ```python
    print(iexec('print(9*9)'))
    ```
    """
    if import_pypipr:
        python_syntax = f"from pypipr.pypipr import *\n\n{python_syntax}"

    stdout_backup = sys.stdout

    sys.stdout = io.StringIO()
    exec(python_syntax)
    output = sys.stdout.getvalue()

    sys.stdout = stdout_backup

    return output


def is_valid_url(path):
    """
    Mengecek apakah path merupakan URL yang valid atau tidak.
    Cara ini merupakan cara yang paling efektif.

    ```python
    print(is_valid_url("https://chat.openai.com/?model=text-davinci-002-render-sha"))
    print(is_valid_url("https://chat.openai.com/?model/=text-dav/inci-002-render-sha"))
    ```
    """
    return bool(__is_valid_url__regex__.fullmatch(path))


def iopen(path, data=None, regex=None, css_select=None, xpath=None, file_append=False):
    """
    Membaca atau Tulis pada path yang bisa merupakan FILE maupun URL.

    Baca File :
    - Membaca seluruh file.
    - Jika berhasil content dapat diparse dengan regex.
    - Apabila File berupa html, dapat diparse dengan css atau xpath.

    Tulis File :
    - Menulis pada file.
    - Jika file tidak ada maka akan dibuat.
    - Jika file memiliki content maka akan di overwrite.

    Membaca URL :
    - Mengakses URL dan mengembalikan isi html nya berupa teks.
    - Content dapat diparse dengan regex, css atau xpath.

    Tulis URL :
    - Mengirimkan data dengan metode POST ke url.
    - Jika berhasil dan response memiliki content, maka dapat diparse dengan regex, css atau xpath.


    ```python
    # FILE
    print(iopen("__iopen.txt", "mana aja"))
    print(iopen("__iopen.txt", regex="(\w+)"))
    # URL
    print(iopen("https://www.google.com/", css_select="a"))
    print(iopen("https://www.google.com/", dict(coba="dulu"), xpath="//a"))
    ```
    """
    path = to_str(path)
    content = ""

    if is_valid_url(path):
        req = dict(
            url=path,
            headers={
                "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Mobile Safari/537.36"
            },
        )

        if data:
            req["data"] = urllib.parse.urlencode(data).encode()

        req = urllib.request.Request(**req)

        # Connect to URL
        try:
            with urllib.request.urlopen(req) as url_open:
                content = url_open.read().decode()
        except Exception as e:
            # print(f"An error occurred: {str(e)}")
            return False

    else:
        # Write File
        if data is not None:
            mode = "a" if file_append else "w"
            with open(path, mode, encoding="utf-8") as f:
                content = f.write(data)
        # Read File
        else:
            try:
                with open(path, "r") as f:
                    content = f.read()
            except Exception as e:
                # print(f"An error occurred: {str(e)}")
                return False

    """ Parse """
    if regex:
        return re.findall(regex, content)
    if css_select:
        return lxml.html.fromstring(content).cssselect(css_select)
    if xpath:
        return lxml.html.fromstring(content).xpath(xpath)

    """ Return """
    return content


def serialize_html(data, indent=None):
    """
    Serialisasi python variabel menjadi HTML.
    ```
    List -> <ul>...</ul>
    Dict -> <table>...</table>
    ```

    ```python
    data = {
        'abc': 123,
        'list': [1, 2, 3, 4, 5],
        'dict': {'a': 1, 'b':2, 'c':3},
    }
    print(serialize_html(data))
    ```
    """

    def to_ul(data):
        ul = lxml.etree.Element("ul")
        for i in data:
            li = lxml.etree.SubElement(ul, "li")
            li.append(to_html(i))
        return ul

    def to_table(data: dict):
        table = lxml.etree.Element("table")
        tbody = lxml.etree.SubElement(table, "tbody")
        for i, v in data.items():
            tr = lxml.etree.SubElement(tbody, "tr")
            th = lxml.etree.SubElement(tr, "th")
            th.text = str(i)
            td = lxml.etree.SubElement(tr, "td")
            td.append(to_html(v))
        return table

    def to_text(data):
        span = lxml.etree.Element("span")
        span.text = str(data)
        return span

    def to_html(data):
        struct = {
            dict: to_table,
            list: to_ul,
            tuple: to_ul,
            set: to_ul,
        }
        return struct.get(type(data), to_text)(data)

    html = to_html(data)
    if indent:
        lxml.etree.indent(html, space=" " * indent)
    return lxml.etree.tostring(html, pretty_print=True, encoding="unicode")


def str_cmp(t1, t2):
    """
    Membandingakan string secara incase-sensitive menggunakan lower().
    Lebih cepat dibandingkan upper(), casefold(), re.fullmatch(), len().
    perbandingan ini sangat cepat, tetapi pemanggilan fungsi ini membutuhkan
    overhead yg besar.
    ```python
    print(str_cmp('teks1', 'Teks1'))
    ```
    """
    return t1.lower() == t2.lower()


def unserialize_html(html):
    """
    Mengambil data yang berupa list `<ul>`, dan table `<table>` dari html
    dan menjadikannya data python berupa list.
    setiap data yang ditemukan akan dibungkus dengan tuple sebagai separator.
    ```
    list (<ul>)     -> list         -> list satu dimensi
    table (<table>) -> list[list]   -> list satu dimensi didalam list
    ```
    apabila data berupa ul maka dapat dicek type(data) -> html_ul
    apabila data berupa ol maka dapat dicek type(data) -> html_ol
    apabila data berupa dl maka dapat dicek type(data) -> html_dl
    apabila data berupa table maka dapat dicek type(data) -> html_table

    ```python
    pprint.pprint(unserialize_html(iopen("https://harga-emas.org/")), depth=10)
    pprint.pprint(unserialize_html(iopen("https://harga-emas.org/1-gram/")), depth=10)
    ```
    """

    def xpath(e, x):
        """
        Fungsi ini sangat krusial/menentukan. Fungsi ini dibuat
        supaya xpath yang diberikan diproses dari element saat ini.
        Sedangkan xpath pada element lxml akan mengecek syntax xpath dari
        root paling awal document.
        """
        if not isinstance(e, str):
            e = lxml.html.tostring(e, encoding="unicode")
        e = lxml.html.fromstring(e)
        return (e, e.xpath(x))

    def parse(e):
        parser = {
            "ul": parse_ul,
            "ol": parse_ol,
            "dl": parse_dl,
            "table": parse_table,
        }
        try:
            return parser[e.tag.lower()](e)
        except:
            raise Exception("Tidak ditemukan parse fungsi untuk element : ", e)

    def parse_list(ul):
        """
        Simple parse html list.
        """
        result = []
        _, li = xpath(ul, "li")
        for i in li:
            u = unserialize_html(i)
            t = i.text.strip() if i.text else ""
            if t and t != u:
                result.append({t: u})
            else:
                result.append(u)
        return result

    def parse_ul(ul):
        return html_ul(parse_list(ul))

    def parse_ol(ol):
        return html_ol(parse_list(ol))

    def parse_dl(dl):
        """
        Simple parse dl-dt-dd.
        """
        result = html_dl()
        _, di = xpath(dl, "dt|dd")
        d = iter(di)
        try:
            while True:
                i = next(d)
                k = i.tag.lower()
                v = unserialize_html(i)
                if k == "dt":
                    result.append(["", []])
                    result[-1][0] = v
                elif k == "dd":
                    result[-1][-1].append(v)
        except:
            pass

        return result

    def parse_table(table):
        """
        Mengambil children tr dari table.
        tr diambil dari thead atau tbody atau langsung tr.
        tr dari thead atau tbody akan dianggap sama.
        """
        result = html_table()
        _, tr = xpath(table, "//tr[not(ancestor::tr)]")
        for itr in tr:
            d = []
            _, td = xpath(itr, "th|td")
            for itd in td:
                d.append(unserialize_html(itd))
            result.append(d.copy())
        return result

    def text_content(e):
        """
        mengambil semua text dalam element secara recursive.
        karena tidak ditemukan data dalam element.
        """
        return implode(e.itertext(), str_strip=True)

    element, childs = xpath(
        html,
        "//*[self::ul | self::ol | self::dl | self::table][not(ancestor::ul | ancestor::ol | ancestor::dl | ancestor::table)]",
    )
    if childs:
        return tuple((parse(data) for data in childs))
    else:
        return text_content(element)


class html_ul(list):
    """
    Class ini digunakan untuk serialize dan unserialize html
    """

    pass


class html_ol(list):
    """
    Class ini digunakan untuk serialize dan unserialize html
    """

    pass


class html_dl(list):
    """
    Class ini digunakan untuk serialize dan unserialize html
    """

    pass


class html_table(list):
    """
    Class ini digunakan untuk serialize dan unserialize html
    """

    pass


if __name__ == "__main__":
    print_colorize("Anda menjalankan module pypipr", color=colorama.Fore.RED)
