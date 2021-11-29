#include "helpers.h"
#include <getopt.h>
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
  for (int i = 0; i < height; i++)
  {
      for (int  j = 0; j < width; j++)
      {
          int average = round((image[i][j].rgbtBlue + image[i][j].rgbtGreen + image[i][j].rgbtRed) / 3.0f);
          //hard code average
          image[i][j].rgbtBlue = average;
          image[i][j].rgbtGreen = average;
          image[i][j].rgbtRed = average;
      }
  }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    
    int widthInterval = floor(width / 2.0f);
    
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < widthInterval; j++)
        {
            //swap current cell with opposite cell; use a temp (leftmost with rightmost)
            RGBTRIPLE temp = image[i][j];
            image[i][j] = image[i][width-j];
            image[i][width-j] = temp;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    return;
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    return;
}
