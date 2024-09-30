from byuimage import Image
import sys


def show_image(args, file):
    if validate_commands(args[1:]):
        Image(file).show()
    return


def collage(args, file1, file2, file3, file4, output_file, weight):
    old_image1 = Image(file1)
    old_image2 = Image(file2)
    old_image3 = Image(file3)
    old_image4 = Image(file4)
    weight = int(weight)
    collage_image = Image.blank(((old_image1.width * 2)+weight*3), ((old_image1.height*2)+weight*3))
    for pixel in collage_image:
        pixel.red = 0
        pixel.green = 0
        pixel.blue = 0

    for y in range(old_image1.height):
        for x in range(old_image1.width):
            old_pixel = old_image1.get_pixel(x, y)
            bordered_pixel = collage_image.get_pixel(x + weight, y + weight)
            bordered_pixel.red = old_pixel.red
            bordered_pixel.green = old_pixel.green
            bordered_pixel.blue = old_pixel.blue

    for y in range(old_image2.height):
        for x in range(old_image2.width):
            old_pixel = old_image2.get_pixel(x, y)
            bordered_pixel = collage_image.get_pixel(x + weight*2 + old_image1.width, y + weight)
            bordered_pixel.red = old_pixel.red
            bordered_pixel.green = old_pixel.green
            bordered_pixel.blue = old_pixel.blue

    for y in range(old_image3.height):
        for x in range(old_image3.width):
            old_pixel = old_image3.get_pixel(x, y)
            bordered_pixel = collage_image.get_pixel(x + weight, y + weight*2 + old_image1.height)
            bordered_pixel.red = old_pixel.red
            bordered_pixel.green = old_pixel.green
            bordered_pixel.blue = old_pixel.blue

    for y in range(old_image4.height):
        for x in range(old_image4.width):
            old_pixel = old_image4.get_pixel(x, y)
            bordered_pixel = collage_image.get_pixel(x + weight*2 + old_image1.width, y + weight*2 + old_image1.height)
            bordered_pixel.red = old_pixel.red
            bordered_pixel.green = old_pixel.green
            bordered_pixel.blue = old_pixel.blue
    collage_image.save(output_file)
    return collage_image


def mirrored(filename, output_file):
    old_image = Image(filename)
    new_image = Image.blank(old_image.width, old_image.height)
    for y in range(0, old_image.height):
        for x in range(0, old_image.width):
            flipped_x = old_image.width - x - 1
            found_pixel = old_image.get_pixel(x, y)
            new_pixel = new_image.get_pixel(flipped_x, y)
            new_pixel.red = found_pixel.red
            new_pixel.green = found_pixel.green
            new_pixel.blue = found_pixel.blue
    new_image.save(output_file)
    return new_image


def flipped(filename, output_file):
    flipped_image = Image(filename)
    new_image = Image.blank(flipped_image.width, flipped_image.height)
    for y in range(0, flipped_image.height):
        for x in range(0, flipped_image.width):
            flipped_y = flipped_image.height - y - 1
            found_pixel = flipped_image.get_pixel(x, y)
            new_pixel = new_image.get_pixel(x, flipped_y)
            new_pixel.red = found_pixel.red
            new_pixel.green = found_pixel.green
            new_pixel.blue = found_pixel.blue
    new_image.save(output_file)
    return new_image


def make_borders(args, filename, output_file, weight, red, green, blue):
    old_image = Image(filename)
    weight = int(weight)
    bordered_image = Image.blank(old_image.width + weight*2, old_image.height + weight*2)
    for pixel in bordered_image:
        pixel.red = red
        pixel.green = green
        pixel.blue = blue

    for y in range(old_image.height):
        for x in range(old_image.width):
            old_pixel = old_image.get_pixel(x, y)
            bordered_pixel = bordered_image.get_pixel(x + weight, y + weight)
            bordered_pixel.red = old_pixel.red
            bordered_pixel.green = old_pixel.green
            bordered_pixel.blue = old_pixel.blue
    bordered_image.save(output_file)
    return bordered_image


def grayscale(filename, output_file):
    old_image = Image(filename)
    new_image = Image.blank(old_image.width, old_image.height)
    for x in range(old_image.width):
        for y in range(old_image.height):
            pixel = old_image.get_pixel(x, y)
            average = (pixel.red + pixel.green + pixel.blue) / 3
            new_pixel = new_image.get_pixel(x, y)
            new_pixel.red = average
            new_pixel.green = average
            new_pixel.blue = average
    new_image.save(output_file)
    return new_image


def sepia(filename, output_file):
        sepia_image = Image(filename)
        for y in range(sepia_image.height):
            for x in range(sepia_image.width):
                pixel = sepia_image.get_pixel(x, y)
                true_red = 0.393 * pixel.red + 0.769 * pixel.green + 0.189 * pixel.blue
                true_green = 0.349 * pixel.red + 0.686 * pixel.green + 0.168 * pixel.blue
                true_blue = 0.272 * pixel.red + 0.534 * pixel.green + 0.131 * pixel.blue
                pixel.red, pixel.blue, pixel.green = true_red, true_blue, true_green
        sepia_image.save(output_file)
        return sepia_image


def darken(args, filename, output_file, percent):
    if validate_commands(args[1:]):
        darken_image = Image(filename)
        for pixel in darken_image:
            pixel.red = pixel.red * (1-percent)
            pixel.green = pixel.green * (1 - percent)
            pixel.blue = pixel.blue * (1 - percent)
        darken_image.save(output_file)
        return darken_image


def validate_commands(args):
    if args[0] == '-d':
        return len(args) >= 2
    if args[0] == '-k':
        return len(args) >= 3
    if args[0] in ['-s', '-g', '-b', '-f', '-m', '-c', '-y']:
        return True


def detect_green(pixel, threshold, factor):
    factor = float(factor)
    threshold = float(threshold)
    average = (pixel.red + pixel.green + pixel.blue) / 3
    if pixel.green >= factor * average and pixel.green > threshold:
        return True
    else:
        return False


def green_screen(foreground, background, threshold, factor):
    final = Image.blank(background.width, background.height)
    for y in range(background.height):
        for x in range(background.width):
            fp = final.get_pixel(x, y)
            bp = background.get_pixel(x, y)
            fp.red = bp.red
            fp.green = bp.green
            fp.blue = bp.blue

    for y in range(foreground.height):
        for x in range(foreground.width):
            fp = foreground.get_pixel(x, y)
            if not detect_green(fp, threshold, factor):
                np = final.get_pixel(x, y)
                np.red = fp.red
                np.green = fp.green
                np.blue = fp.blue
    return final


def main(args):
    if validate_commands(args[1:]):
        if args[1] == '-d':
            show_image(args, args[2])
        if args[1] == '-k':
            darken(args, args[2], args[3], float(args[4])).show()
        if args[1] == '-s':
            sepia(args, args[2], args[3]).show()
        if args[1] == '-g':
            grayscale(args, args[2], args[3]).show()
        if args[1] == '-b':
            make_borders(args, args[2], args[3], args[4], args[5], args[6], args[7]).show()
        if args[1] == '-f':
            flipped(args, args[2], args[3]).show()
        if args[1] == '-m':
            mirrored(args, args[2], args[3]).show()
        if args[1] == '-c':
            collage(args, args[2], args[3], args[4], args[5], args[6], args[7]).show()
        if args[1] == '-y':
            green_screen_it(args, args[2], args[3], args[4], args[5], args[6]).show()


def green_screen_it(args, foreground, background, output, threshold, factor):
    foreground_img = Image(foreground)
    background_img = Image(background)
    screen_img = green_screen(foreground_img, background_img, threshold, factor)
    screen_img.save(output)
    return screen_img


if __name__ == '__main__':
    main(sys.argv)