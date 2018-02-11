import os
import random
import shutil
import math
import copy
import glob
import settings
import helpers


def get_items():
    labels_list = glob.glob(settings.upload_folder + '*')

    labels_json = []

    for label in labels_list:
        label_object = {
            'name': label.split('/')[-1],
            'items': []
        }

        items_list = glob.glob(label + '/*')
        types = ('.png', '.jpg', '.jpeg')

        if len(items_list) > 0:
            for item in items_list:   
                item_object = {
                    'id': item.split('/')[-1].split(types)[0],
                    'image_url': item
                }
                label_object['items'].append(item_object)

            labels_json.append(label_object)
    return labels_json


labels_json = get_items()


def process_tags(data):
    path = settings.upload_folder + data['tag'][0] + '/'
    if not os.path.exists(path):
        os.makedirs(path)
    for item in data['ids[]']:
        print 'Moving item ' + item
        old_item_path = helpers.find(item + '.*', settings.upload_folder)
        new_item_path = path + old_item_path.split('/')[-1]
        os.rename(old_item_path, new_item_path)


def delete_items(data):
    print 1
    # for item_id in data['ids[]']:
    #     path = helpers.find(item_id + '.*', settings.upload_folder)
    #     if path:
    #         os.remove(path)
    for item_id in data['ids[]']:
        if path:
            print(path)
            os.remove(path)


def get_suggestions(custom_path):
    labels_list = glob.glob(custom_path + '*')
    untagged_items_paths = glob.glob(settings.upload_folder + '/untagged/*')
    untagged_items = []
    for path in untagged_items_paths:
        untagged_items.append(path.split('/')[-1])

    labels_json = []

    for label in labels_list:
        label_object = {
            'name': label.split('/')[-1],
            'items': []
        }

        items_list = glob.glob(label + '/*')

        if len(items_list) > 0:
            for item in items_list:
                if item.split('/')[-1] in untagged_items:
                    item_object = {
                        'id': item.split('/')[-1].split('.')[0],
                        'image_url': item
                    }
                    label_object['items'].append(item_object)
            if len(label_object['items']) > 0:
                labels_json.append(label_object)

    return labels_json


def paginate_tagged_items(tagged_items, items_per_page=100):
    items_count = sum(len(tag['items']) for tag in tagged_items)

    pages_count = int(math.ceil(items_count / float(items_per_page)))

    # We can return now if there's only going to be one page
    if items_count <= items_per_page:
        return [tagged_items]

    paginated_tagged_items = []

    # For every page, create a subset of tagged_items with the correct number
    # of items
    for page_index in range(0, pages_count):
        # Get the shape of tagged_items
        # It's an array of how many items there are per each tag
        tagged_items_shape = []
        for tag in tagged_items:
            tagged_items_shape.append(len(tag['items']))

        this_page_item_count = 0
        tagged_items_index = 0

        # Go through each tag's item list until we fill the quota for this page
        while this_page_item_count <= items_per_page and tagged_items_index < len(tagged_items):

            this_page_item_count += tagged_items_shape[tagged_items_index]
            tagged_items_index += 1

        this_page = copy.deepcopy(tagged_items[0:tagged_items_index])

        # We might have overshot, so need to cut the remainder from the last
        # tag's list
        if this_page_item_count > items_per_page:
            tagged_items_index = tagged_items_index - 1
            difference = items_per_page - this_page_item_count

            # Remove as many as we need from the last tag in the page
            if this_page[-1]['items'][:difference] == []:
                this_page.remove(this_page[-1])
            else:
                this_page[-1]['items'] = this_page[-1]['items'][:difference]

            # Keep the ones we removed
            tagged_items[tagged_items_index]['items'] = tagged_items[
                tagged_items_index]['items'][difference:]

        paginated_tagged_items.append(this_page)
        tagged_items = tagged_items[tagged_items_index:]

    return paginated_tagged_items


def get_num_pages(tagged_items, items_per_page=100, tag='all'):

    if tag == 'all':
        items_count = sum(len(tag['items']) for tag in tagged_items)
    else:
        try:
        #if len(tagged_items) > 0:
            items_count = len([item for item in tagged_items if item[
                          'name'] == tag][0]['items'])
        #else:
        except IndexError:
            items_count = 0
    pages_count = int(math.ceil(items_count / float(items_per_page)))
    print pages_count, 'number of pages'
    return pages_count


def get_page(tagged_items, page_num, items_per_page=100):
    index = page_num - 1
    items = paginate_tagged_items(tagged_items, items_per_page)
    if index >= len(items):
        index = 0
    return items[index]


def get_tag(tags_list, tag='untagged'):
    for aTag in tags_list:
        if aTag['name'] == tag:
            return [aTag]
    return []


def summarise_items(items):
    summary = {}
    for tag in items:
        summary[tag['name']] = len(tag['items'])
    return summary


def split_train_validation():
    tensorflow_images_path = 'tensorflow_images/'
    master_path = tensorflow_images_path + 'master/'
    split_files_path = tensorflow_images_path + 'split/'
    try:
        shutil.rmtree(split_files_path + 'training/')
    except OSError:
        print 'Training directory didn\'t exist'
    try:
        shutil.rmtree(split_files_path + 'validation/')
    except OSError:
        print 'Validation directory didn\'t exist'
    paths = helpers.find_multi('*', settings.upload_folder)
    items = {}
    ignore = ['.DS_Store', 'untagged']
    for path in paths:
        if not any(string in path for string in ignore):
            split_path = path.split('/')
            tag = split_path[-2]
            filename = split_path[-1]
            items.setdefault(tag, []).append(filename)

    # Copy all images to new directory space
    for tag in items:
        helpers.copy_files([settings.upload_folder + tag + '/' + filename for filename in items[tag]],
                           master_path + tag + '/')

    # Divide images into training/validation 80/20
    # If fewer than 5 images, put them all into training
    for tag in items:
        if len(items[tag]) > 0:
            random.shuffle(items[tag])
            training = items[tag]
            validation = []
            while len(training) >= 50 and len(training) > len(validation) * 4:
                validation.append(training.pop())

            helpers.copy_files([master_path + tag + '/' + filename for filename in training],
                               '%straining/%s/' % (split_files_path, tag))
            helpers.copy_files([master_path + tag + '/' + filename for filename in validation],
                               '%svalidation/%s/' % (split_files_path, tag))


def get_items_count(min_count=1000):
    items = get_items()
    count = 0
    for tag in items:
        num_items = len(tag['items'])
        if num_items > min_count:
            count += num_items
    return count
