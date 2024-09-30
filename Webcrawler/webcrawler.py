import requests
import bs4
import matplotlib.pyplot
import re
import sys
from LinkValidator import LinkValidator
import shutil
import image_processing


def construct_url(base_url, relative_url):
    if base_url.endswith('/'):
        base_url = base_url[:-1]

    if relative_url.startswith('/'):
        return base_url + relative_url
    else:
        return '/'.join(base_url.split('/')[:-1]) + '/' + relative_url


def parse_robots(domain_name):
    """Returns the list of paths to exclude from domain_name's robots.txt file."""
    domain = domain_name.split('//') if '//' in domain_name else domain_name
    sections = domain[1].split('/')
    base_domain = f'{domain[0]}//{sections[0]}'

    response_obj = requests.get(base_domain + '/robots.txt')
    forbidden_stuff = re.findall(r"Disallow: (.*)", response_obj.text)
    return forbidden_stuff


def validate_commands(args):
    if args[0] in ['-c', '-p']:
        return True
    elif args[0] == '-i':
        if args[3] in ['-s', '-g', '-m', '-f']:
            return True
        else:
            raise IndexError(f'{args[3]} is an invalid arguments.\nValid arguments for this command are:\n-s\n-g\n-m\n-f\nPLease choose a valid command from the provided above.')
    else:
        raise IndexError(f'{args[0]} is an invalid arguments.\nValid arguments for this project are:\n-c\n-p\n-i\nPLease choose a valid command from the provided above.')


def process(link_validator, current_url, link):
    if link is not None:
        link_no_hash = link.split('#')[0]
        link_to_process = link_no_hash if '#' in link else link
        if link_to_process.startswith('http://') or link_to_process.startswith('https://'):
            return link_to_process
        elif link_to_process.startswith('/'):
            return link_validator.domain + link_to_process
        elif link_to_process.startswith('#'):
            return current_url + link_to_process
        else:
            return construct_url(current_url, link_to_process)
    else:
        raise TypeError('The "link" variable is None. Please remedy this.')


def counting_links(start_url, output_1, output_2):
    visited = {}
    links = [start_url]
    disallows = parse_robots(start_url)
    domain = start_url.split('//') if '//' in start_url else start_url
    sections = domain[1].split('/')
    base_domain = f'{domain[0]}//{sections[0]}'
    link_validator = LinkValidator(base_domain, disallows)
    index = 0
    while index < len(links):
        url = links[index]

        if url in visited:
            visited[url] += 1
        else:
            visited[url] = 1
            if link_validator.can_follow_link(url):
                page = requests.get(url)
                html = bs4.BeautifulSoup(page.text, "html.parser")

                for tag in html.find_all('a'):
                    href = tag.get('href')
                    if href is not None:
                        processed_link = process(link_validator, url, href)
                        links.append(processed_link)
        index += 1
    count_values = list(visited.values())
    max_count = max(count_values)
    bins = list(range(1, max_count + 2))
    counts, bin_edges, _ = matplotlib.pyplot.hist(count_values, bins=bins)
    matplotlib.pyplot.savefig(output_1)
    matplotlib.pyplot.close()
    with open(output_2, 'w') as file:
        for i in range(len(counts)):
            file.write(f"{bin_edges[i]:.1f},{counts[i]:.1f}\n")


def table_stuff(url, outfile_1, outfile_2):
    page = requests.get(url)
    if page.status_code != 200:
        raise TypeError('The URL inputed is invalid, please double check for any input errors.')
    html = bs4.BeautifulSoup(page.text, "html.parser")
    table = html.find("table", id="CS111-Project4b")
    x_axis = []
    y_axis = []
    colors = ['blue', 'green', 'red', 'black']
    for row in table.find_all('tr'):
        columns = row.find_all('td')
        x_axis.append(float(columns[0].text))
        for i, column in enumerate(columns[1:]):
            if i >= len(y_axis):
                y_axis.append([])
            y_axis[i].append(float(column.text))
    for y_group in y_axis:
        matplotlib.pyplot.plot(x_axis, y_group, color=colors.pop(0))
    matplotlib.pyplot.savefig(outfile_1)
    matplotlib.pyplot.close()
    with open(outfile_2, 'w') as file:
        for i, x_val in enumerate(x_axis):
            row = [str(x_val)]
            row.extend(str(y[i]) for y in y_axis)
            file.write(','.join(row) + '\n')


def image_stuff(url, outfile_prefix, filter):
    page = requests.get(url)
    if page.status_code != 200:
        raise TypeError('The URL inputed is invalid, please double check for any input errors.')
    html = bs4.BeautifulSoup(page.text, "html.parser")
    image_links = []
    for image_tag in html.find_all("img", src=True):
        image_url = image_tag['src']
        if not bool(re.match(r"^https?://", image_url)):
            image_url = construct_url(url, image_url)
        image_links.append(image_url)
    for image_url in image_links:
        part_i_want = image_url.split('/')[-1]
        response = requests.get(image_url, stream=True)
        with open(part_i_want, 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        del response
        if filter == '-s':
            image_processing.sepia(part_i_want, f'{outfile_prefix}{part_i_want}')
        elif filter == '-g':
            image_processing.grayscale(part_i_want, f'{outfile_prefix}{part_i_want}')
        elif filter == '-f':
            image_processing.flipped(part_i_want, f'{outfile_prefix}{part_i_want}')
        elif filter == '-m':
            image_processing.mirrored(part_i_want, f'{outfile_prefix}{part_i_want}')
        else:
            raise IndexError('Invalid operation. Valid Operations are:\n-s\n-g\-f\-m\nPlease choose a valid operation from the list provided.')


def main(args):
    if validate_commands(args[1:]):
        if args[1] == '-c':
            counting_links(args[2], args[3], args[4])
        if args[1] == '-p':
            table_stuff(args[2], args[3], args[4])
        if args[1] == '-i':
            image_stuff(args[2], args[3], args[4])


if __name__ == "__main__":
    main(sys.argv)
